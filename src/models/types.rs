#[derive(SqlType)]
#[postgres(type_name = "Tusee_access")]
pub struct Tusee_access_type;

#[derive(Debug, AsExpression, FromSqlRow)]
#[sql_type = "Tusee_access_type"]
pub enum Tusee_access {
    boolean,
    text,
    textlong
}

#[derive(SqlType)]
pub enum Tusee_permissions_types {

}

#[derive(SqlType)]
pub enum Tusee_permissions_type {
    boolean,
    text,
    textlong
}

#[derive(SqlType)]
pub enum Tusee_settings_type {
    boolean,
    text,
    textlong
}