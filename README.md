#  ❄️ Snow Instructor ❄️

<div align="center">
<img src="https://raw.githubusercontent.com/FlorianWilhelm/snow-instructor/main/assets/logo-woman.png" alt="Snow Instructor logo" width="500" role="img">
</div>

Artic Snowflake instructor that teaches you about Snowflake's capabilities by playfully answering quiz questions.

## 💫 Features

With this full-fledged AI-based Streamlit Application on Snowflake, you'll learn about:

* [Snowpark's Python API]
* [Snowflake's Cortex AI capabilities] and especially the [Snowflake Arctic LLM]
* [Multi-page Streamlit application]
* [Streamlit Deployment on Snowflake]
* [Snowflake CLI]

## ⛷️ Getting Started

1. If you are a new Snowflake user, [register a 30-day free trial Snowflake account].
   Choose the enterprise edition, AWS as cloud provider and region AWS US West 2 (Oregon),
   as [Snowflake Arctic is currently only available in this region].
2. Create a Snowflake configuration file under `~/.snowflake/connections.toml` with:

    ```ini
    [default]
    account = "YOUR_ACCOUNT"
    user = "YOUR_USER_NAME"
    password = "YOUR_PASSWORD"
    role = "accountadmin"
    warehouse = "COMPUTE_WH"
    database = "SNOWINSTRUCTOR"
    schema = "public"
    ```

3. Clone this repository into a directory `snowflake-instuctor`.
4. Install [hatch] globally, e.g. with [pipx], i.e. `pipx install hatch`.
5. Let our spider crawl the [Snowflake documentation] and upload it into a Snowflake table with:

   ```bash
   hatch run crawl-snow-docs
   ```

   This needs to be done exactly once and will also make sure that your connection works.
6. To check if our Snowflake Instructor works on the command-line, try:

   ```bash
   hatch run cli-quiz
   ```

7. To start the [Streamlit] client locally on your machine, run:

   ```bash
   hatch run snow-instructor
   ```

8. To deploy everything on Snowflake, run within the root of this repo:

   ```bash
   hatch run prep-deployment  # to setup the warehouse, etc.
   hatch run deploy-streamlit
   ```

   And open up the URL shown in the output of the last command.


## 🛠️ Development

To set up [hatch] and [pre-commit] for the first time:

1. install [hatch] globally, e.g. with [pipx], i.e. `pipx install hatch`,
2. make sure `pre-commit` is installed globally, e.g. with `pipx install pre-commit`.

A special feature that makes hatch very different from other familiar tools is that you almost never
activate, or enter, an environment. Instead, you use `hatch run env_name:command` and the `default` environment
is assumed for a command if there is no colon found. Thus you must always define your environment in a declarative
way and hatch makes sure that the environment reflects your declaration by updating it whenever you issue
a `hatch run ...`. This helps with reproducability and avoids forgetting to specify dependencies since the
hatch workflow is to specify everything directly in [pyproject.toml](pyproject.toml). Only in rare cases, you
will use `hatch shell` to enter the `default` environment, which is similar to what you may know from other tools.

To get you started, use `hatch run test:cov` or `hatch run test:no-cov` to run the unitest with or without coverage reports,
respectively. Use `hatch run lint:all` to run all kinds of typing and linting checks. Try to automatically fix linting
problems with `hatch run lint:fix` and use `hatch run docs:serve` to build and serve your documentation.
You can also easily define your own environments and commands. Check out the environment setup of hatch
in [pyproject.toml](pyproject.toml) for more commands as well as the package, build and tool configuration.

The environments defined by hatch are configured to generate lock files using [hatch-pip-compile] under `locks`.
To upgrade all packages in an environment like `test`, just run `hatch run test:upgrade-all`. To upgrade specific
packages, type `hatch run test:upgrade-pkg pkg1,pkg2`.

## 🙏 Credits

This package was created with [The Hatchlor] project template.

[The Hatchlor]: https://github.com/florianwilhelm/the-hatchlor
[pipx]: https://pypa.github.io/pipx/
[hatch]: https://hatch.pypa.io/
[pre-commit]: https://pre-commit.com/
[hatch-pip-compile]: https://github.com/juftin/hatch-pip-compile
[register a 30-day free trial Snowflake account]: https://trial.snowflake.com/?owner=SPN-PID-545753
[Snowflake Arctic is only available in this region]: https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#label-cortex-llm-availability
[Snowflake documentation]: https://docs.snowflake.com/
[Streamlit]: https://streamlit.io/
[Snowpark's Python API]: https://docs.snowflake.com/en/developer-guide/snowflake-python-api/snowflake-python-overview
[Snowflake's Cortex AI capabilities]: https://docs.snowflake.com/en/user-guide/snowflake-cortex/overview
[Snowflake Arctic LLM]: https://www.snowflake.com/en/data-cloud/arctic/
[Mulit-page Streamlit application]: https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
[Streamlit Deployment on Snowflake]: https://www.snowflake.com/en/data-cloud/overview/streamlit-in-snowflake/
[Snowflake CLI]: https://docs.snowflake.com/developer-guide/snowflake-cli-v2/index
