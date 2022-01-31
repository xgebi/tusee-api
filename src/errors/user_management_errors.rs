#[derive(Debug)]
pub(crate) enum RegistrationError {
    AlreadyRegistered,
    DatabaseError,
}

impl std::error::Error for RegistrationError {}

impl std::fmt::Display for RegistrationError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            RegistrationError::AlreadyRegistered => write!(f, "User already registered."),
            RegistrationError::DatabaseError => write!(f, "Couldn't register.")
        }
    }
}

#[derive(Debug)]
pub(crate) enum CredentialsError {
    FailedCreatingCookie,
    NonExistentCookie,
    FailedExtractingCookie,
    FailedCreatingTotpQr,
}

impl std::error::Error for CredentialsError {}

impl std::fmt::Display for CredentialsError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            CredentialsError::FailedCreatingCookie => write!(f, "Couldn't create secured cookie."),
            CredentialsError::NonExistentCookie => write!(f, "Cookie doesn't exist."),
            CredentialsError::FailedExtractingCookie => write!(f, "Couldn't extract secured cookie."),
            CredentialsError::FailedCreatingTotpQr => write!(f, "Couldn't create QR code.")
        }
    }
}
