#[derive(SqlType)]
#[postgres(type_name = "Tusee_access")]
pub struct Tusee_access_type;

#[derive(Debug, AsExpression, FromSqlRow)]
#[sql_type = "Tusee_access_type"]
pub enum Tusee_access {
    Boolean,
    Text,
    Textlong
}

#[derive(SqlType)]
pub enum Tusee_permissions_types {

}

#[derive(SqlType)]
#[postgres(type_name = "Tusee_permission")]
pub struct Tusee_permission_type;

#[derive(Debug, AsExpression, FromSqlRow)]
#[sql_type = "Tusee_permission_type"]
pub enum Tusee_permission {
    Boolean,
    Text,
    Textlong
}

#[derive(SqlType)]
#[postgres(type_name = "Tusee_settings")]
pub struct Tusee_settings_type;

#[derive(Debug, AsExpression, FromSqlRow)]
#[sql_type = "Tusee_settings_type"]
pub enum Tusee_settings {
    Boolean,
    Text,
    Textlong
}