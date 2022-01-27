use serde::{Serialize, Deserialize};

#[derive(Deserialize, Serialize, Debug, Clone)]
pub(crate) struct Token {
    pub(crate) password: String,
    pub(crate) email: String,
    pub(crate) expiry_date: u64,
    pub(crate) mfa_verified: bool,
}