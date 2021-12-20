#[derive(Queryable)]
pub(crate) struct Post {
    pub(crate) uuid: String,
    pub(crate) display_name: String,
    pub(crate) password: String,
    pub(crate) email: String,
    pub(crate) token: String,
    pub(crate) expiry_date: f64,
}