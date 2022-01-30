#[derive(Debug)]
pub(crate) enum RegistrationError {
    AlreadyRegistered,
    DatabaseError,
}

impl std::error::Error for RegistrationError {}

impl std::fmt::Display for RegistrationError {
    fn fmt(&self, f: &mut std::fmt::Formatter)
    -> std::fmt::Result {
        match self {
            RegistrationError::AlreadyRegistered => write!(f, "User already registered."),
            RegistrationError::DatabaseError => write!(f, "Couldn't register.")
        }
    }
}
