use crate::models::types::Tusee_access_type;

#[derive(Queryable)]
pub(crate) struct Settings {
    pub(crate) uuid: String,
    pub(crate) display_name: String,
    pub(crate) settings_value_type: Tusee_access_type,
    pub(crate) settings_value: String,
}