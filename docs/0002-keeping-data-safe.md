# Keeping data safe

**More research is needed**

Use AES, package `aes-gcm` because it was audited.

Password will be used to decrypt something[1].

Something means
1) another key, something like 1Password's Master key
2) individual entries

In both cases, lost password means lost data for user.

## Reasons for #1

| Pros                                                  | Cons                |
|-------------------------------------------------------|---------------------|
| Can be used with more dashboards (individual, shared) | Harder to implement |
|                                                       |                     |

## Reasons for #2
| Pros                                      | Cons                                  |
|-------------------------------------------|---------------------------------------|
| Easier to implement individual dashboards | Harder to implement shared dashboards |
|                                           | A bit less secure                     |