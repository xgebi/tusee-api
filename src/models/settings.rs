#[derive(Queryable)]
pub(crate) struct Settings {
    pub(crate) uuid: String,
    pub(crate) display_name: String,
    pub(crate) settings_value_type: String,
    pub(crate) settings_value: String,
}