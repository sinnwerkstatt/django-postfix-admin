from django.db import connection


class Database:
    def __init__(self):
        self.dbdict = connection.settings_dict

        if 'postgresql' in self.dbdict['ENGINE']:
            driver = "pgsql"
        elif 'mysql' in self.dbdict['ENGINE']:
            driver = "mysql"
        elif 'sqlite3' in self.dbdict['ENGINE']:
            driver = "sqlite"
        else:
            raise Exception('unsupported')
        self.driver = driver

    def dovecot_sql_conf(self):
        connect = f"host={self.dbdict['HOST']} dbname={self.dbdict['NAME']} user={self.dbdict['USER']} password={self.dbdict['PASSWORD']}"
        default_pass_scheme = "BLF-CRYPT"
        password_query = "SELECT name AS username, domain_id AS domain, password FROM mail_mailbox WHERE name = '%n' AND domain_id = '%d' AND active = true;"
        user_query = "SELECT '*:storage=' || quota || 'M' AS quota_rule FROM mail_mailbox WHERE name = '%n' AND domain_id = '%d';"
        iterate_query = "SELECT name AS username, domain_id AS domain FROM mail_mailbox;"

        if self.driver == 'sqlite':
            connect = self.dbdict['NAME']

        elif self.driver == 'mysql':
            user_query = "SELECT concat('*:storage=', quota, 'M') AS quota_rule FROM mail_mailbox WHERE name = '%n' AND domain_id = '%d';"

        retval = [
            f"driver = {self.driver}",
            f"connect = {connect}",
            f"default_pass_scheme = {default_pass_scheme}",
            f"password_query = {password_query}",
            f"user_query = {user_query}",
            f"iterate_query = {iterate_query}",
        ]
        return "\n".join(retval)

    def postfix_sql_conf(self):
        connect = f"user = {self.dbdict['USER']}\npassword = {self.dbdict['PASSWORD']}\nhosts = {self.dbdict['HOST']}\ndbname = {self.dbdict['NAME']}"
        if self.driver == 'sqlite':
            connect = f"dbpath = {self.dbdict['NAME']}"

        alldings = {
            'accounts.cf': "SELECT 1 AS found FROM mail_mailbox WHERE name ='%u' AND domain_id ='%d' AND active=true LIMIT 1;",
            'aliases.cf': "SELECT regexp_replace(targets, '[\\n\\r]+', ',', 'g') AS destination FROM mail_alias WHER name = '%u' AND domain_id='%d' AND active=true;",
            'domains.cf': "SELECT name FROM mail_domain WHERE name='%d';",
            'sender-login-maps.cf': "select name || '@' || domain_id as owns from mail_mailbox where name ='%u' and domain_id ='%d' and active = true union select name || '@' || domain_id as owns from mail_alias where name = '%u' and domain_id='%d' and active=true;",
            'tls-policy.cf': "SELECT policy, params FROM mail_tlspolicy WHERE domain = '%d';"

        }
        ret = ""
        for k,v in alldings.items():
            ret += f"{k}:\n" + "\n".join([connect, v]) + "\n\n"
        return ret
        # return "\n".join([connect,'xx'])


    # TODO: fix 1 != true
