MYSQL_PRODUCTION_SETTINGS = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'main'
}

LOGIN_SETTINGS_INTEGRATION = {
    'base_url': 'https://proteus-test-e2e-bluemoon.aws.proteantecs.com',
    'frontend_url': 'https://proteus-test-e2e-bluemoon.aws.proteantecs.com/app/13358669/overview',
    'pt_admin_user_password': 'AdpT2o23!!',
    'pt_admin_user_name': 'admin@proteantecs.com',
    'user_name': 'testuser@proteantecs.com',
    'user_password': 'pT123456789!',
    'keycloak_url': 'https://keycloak-e2e-bluemoon.aws.proteantecs.com/auth/realms/ProteanDev/protocol/openid-connect/token',
    'keycloak_username': 'admin@proteantecs.com',
    'keycloak_password': 'AdpT2o23!!'
}

PLATFORM_LOGIN_SETTINGS_GREG = {
    'namespace': 'protean',
    'base_url': 'https://proteus-test-protean-greg.gcp.proteantecs.com',
    'frontend_url': 'https://proteus-test-protean-greg.gcp.proteantecs.com/app/22/overview',
    'pt_admin_user_password': 'ZAQ12wsxPTGR1@',
    'pt_admin_user_name': 'admin@proteantecs.com',
    'user_name': 'testuser@proteantecs.com',
    'user_password': 'pT123456789!',
    'keycloak_url': 'https://keycloak-protean-greg.gcp.proteantecs.com/auth/realms/ProteanDev/protocol/openid-connect/token',
    'keycloak_username': 'admin@proteantecs.com',
    'keycloak_password': 'fAyxp%23ysmrh0C4w'
}

PLATFORM_LOGIN_SETTINGS_VERTICA = {
    'frontend_url': 'https://proteus-test-od-victori-bluemoon-b.aws.proteantecs.com/app/2/overview',
    'pt_admin_user_password': 'fAyxp#ysmrh0C4w',
    'pt_admin_user_name': 'admin@proteantecs.com'
}

PLATFORM_LOGIN_SETTINGS_VERTICA_TESTUSER = {
    'namespace': 'od-victori-bluemoon-b',
    'base_url': 'https://proteus-test-od-victori-bluemoon-b.aws.proteantecs.com',
    'frontend_url': 'https://proteus-test-od-victori-bluemoon-b.aws.proteantecs.com/app/2/overview',
    'pt_admin_user_password': 'fAyxp#ysmrh0C4w',
    'pt_admin_user_name': 'admin@proteantecs.com',
    'user_name': 'testuser@proteantecs.com',
    'user_password': 'pT123456789!',   #'fAyxp#ysmrh0C4w'
    'keycloak_url': 'https://keycloak-od-victori-bluemoon-b.aws.proteantecs.com/auth/realms/ProteanDev/protocol/openid-connect/token',
    'keycloak_username': 'admin@proteantecs.com',
    'keycloak_password': 'fAyxp%23ysmrh0C4w'
}

PLATFORM_LOGIN_SETTINGS_DEFAULT = PLATFORM_LOGIN_SETTINGS_GREG

