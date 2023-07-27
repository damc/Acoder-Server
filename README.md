# Server

https://acoder.herokuapp.com

The server-side part of the Acoder app.

## Running the website in the local environment

In order to run the website locally, run

```
./run.sh
```

# Code

The most important part is the `solver` package - it contains the code that actually do the job (generates code through contact with OpenAI API and doing some things on top of that). The Acoder website and API is contained by `server` package.
