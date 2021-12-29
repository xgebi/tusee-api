use crate::models::types::Tusee_access_types;

table! {
    tusee_access_audit_log (uuid) {
        uuid -> Varchar,
        tusee_user -> Nullable<Varchar>,
        ip -> Nullable<Varchar>,
        event -> Nullable<Tusee_access_types>,
    }
}

table! {
    tusee_available_user_boards (uuid) {
        uuid -> Varchar,
        tusee_user -> Nullable<Varchar>,
        board -> Nullable<Varchar>,
    }
}

table! {
    tusee_boards (uuid) {
        uuid -> Varchar,
        name -> Nullable<Text>,
        description -> Nullable<Text>,
        owner -> Nullable<Varchar>,
    }
}

table! {
    tusee_encrypted_keys (uuid) {
        uuid -> Varchar,
        tusee_user -> Nullable<Varchar>,
        key -> Nullable<Text>,
    }
}

table! {
    tusee_permissions_audit_log (uuid) {
        uuid -> Varchar,
        tusee_user -> Nullable<Varchar>,
        ip -> Nullable<Varchar>,
        event -> Nullable<Tusee_permissions_types>,
    }
}

table! {
    tusee_scheduled_blocks (uuid) {
        uuid -> Varchar,
        task -> Nullable<Varchar>,
        start_time -> Nullable<Text>,
        end_time -> Nullable<Text>,
    }
}

table! {
    tusee_settings (settings_name) {
        settings_name -> Varchar,
        display_name -> Varchar,
        settings_value_type -> Tusee_settings_type,
        settings_value -> Varchar,
    }
}

table! {
    tusee_tasks (uuid) {
        uuid -> Varchar,
        creator -> Nullable<Varchar>,
        board -> Nullable<Varchar>,
        description -> Nullable<Text>,
        updated -> Nullable<Text>,
        created -> Nullable<Text>,
    }
}

table! {
    tusee_users (uuid) {
        uuid -> Varchar,
        display_name -> Nullable<Text>,
        password -> Varchar,
        email -> Nullable<Varchar>,
        token -> Nullable<Varchar>,
        expiry_date -> Nullable<Float8>,
    }
}

joinable!(tusee_available_user_boards -> tusee_boards (board));
joinable!(tusee_scheduled_blocks -> tusee_tasks (task));
joinable!(tusee_tasks -> tusee_users (creator));

allow_tables_to_appear_in_same_query!(
    tusee_access_audit_log,
    tusee_available_user_boards,
    tusee_boards,
    tusee_encrypted_keys,
    tusee_permissions_audit_log,
    tusee_scheduled_blocks,
    tusee_settings,
    tusee_tasks,
    tusee_users,
);
