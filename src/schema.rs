table! {
    tusee_access_audit_log (uuid) {
        uuid -> Varchar,
        tusee_user -> Varchar,
        ip -> Varchar,
        event -> Varchar,
    }
}

table! {
    tusee_available_user_boards (uuid) {
        uuid -> Varchar,
        tusee_user -> Varchar,
        board -> Varchar,
    }
}

table! {
    tusee_boards (uuid) {
        uuid -> Varchar,
        name -> Nullable<Text>,
        description -> Nullable<Text>,
        owner -> Varchar,
    }
}

table! {
    tusee_encrypted_keys (uuid) {
        uuid -> Varchar,
        tusee_user -> Varchar,
        key -> Text,
    }
}

table! {
    tusee_permissions_audit_log (uuid) {
        uuid -> Varchar,
        tusee_user -> Varchar,
        ip -> Varchar,
        event -> Varchar,
    }
}

table! {
    tusee_scheduled_blocks (uuid) {
        uuid -> Varchar,
        task -> Varchar,
        start_time -> Text,
        end_time -> Text,
    }
}

table! {
    tusee_settings (settings_name) {
        settings_name -> Varchar,
        display_name -> Varchar,
        settings_value_type -> Varchar,
        settings_value -> Varchar,
    }
}

table! {
    tusee_tasks (uuid) {
        uuid -> Varchar,
        creator -> Varchar,
        board -> Varchar,
        description -> Text,
        updated -> Text,
        created -> Text,
    }
}

table! {
    tusee_users (uuid) {
        uuid -> Varchar,
        display_name -> Text,
        password -> Varchar,
        email -> Varchar,
        token -> Varchar,
        expiry_date -> Float8,
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
