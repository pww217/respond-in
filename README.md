# respond-in

Simple script that parses your inbox and replies based on a template.

## Auth

Currently it pulls LinkedIn credentials from a local json file.

Create a `creds.json` and then enter:
```json
{
"LKDIN_USER": "myemail@gmail.com",
"LKDIN_PW":"SomePassword"
}
```

## Template

Create a `template.txt` and fill it with any plaintext. 

New lines will be honored. Use `template-example.txt` 

The `fname` variable can be used to personalize the salutation.