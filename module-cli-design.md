# Module CLI design

This document describes the module cli usage.

[TOC]



## General

The command line utility is named `module`, and have some actions like `register`, `upgrade`, `download`, etc as sub command to handle the corresponding scenarios.

###  Global options

All the commands in this document may apply to the following options:

##### `--subscription-id` `-s`
Specifies the subscription id for the workspace to operate on.

If not specified, will use the current active subscription id in the az cli environment.

Use the following commands to show or change current subscription in your environment.

* List subscriptions:
  ```bash
  az account list --output table
  ```
  
* Set active subscription:
  ```bash
  az account set --subscription "Subscription Name"
  ```

##### `--resource-group` `-g`
Specifies the resource group name for the workspace to operate on.

If not specified, the default configuration in az cli environment will be used.

Use the following command to set the default resource group name.

```bash
az configure --defaults group=<Resource Group Name>
```

##### `--workspace-name` `-w`
Specifies name of the workspace to operate on.

If not specified, the default configuration in az cli environment will be used.

Use the following command to set the default resource group name.

```bash
az configure --defaults graml_workspaceoup=<Workspace Name>
```

##### `--debug`
Increase logging verbosity to show all debug logs.

##### `--verbose`
Increase logging verbosity. Will show the full data that the CLI retrieved from server.

##### `--output` `-o`
Output format. Allowed values: `json`, `jsonc`, `table`,`tsv`. Default: `json`.

##### `--help` `-h`
Show this help message and exit.



## Usage scenarios

###  module register

Register a module to the given workspace.

To register a module, a **module spec file** and **module implementation code (a.k.a. snapshot)** should be prepared in advance. We call it a **Module Package** in this document later on. 

In the module package, there should be one yaml file to define the module spec. The module spec file could be located in any relative path inside the module package, but it is recommended to be located at the top level folder. The module spec could be with arbitrary file names, but must with a `.yaml` extension.

There can be multiple module spec files inside one module package, but the user will be enforced to specify the module spec path when registering the module via CLI command.

The module package could be located at various location with various format, such as:

* A path to a local folder.
* A path to a local zip file.
* A link to a GitHub repo, could also contain subfolders like: 
* A link to a DevOps build drop url. (Planned to support in the future)



Invoke a module register using the follow command:

```bash
module register path-or-url
               [--spec-file]
               [--set-as-default-version]
```
> The parameters with bracket (e.g. [--spec-file]) indicates that the parameter is optional.

##### `path-or-url`
This is a positional parameter. Specifies the location of the module package.
##### `--spec-file` `-f`
Specifies the path to the spec file. Not needed if the module package contains only one spec file.

##### `--set-as-default-version` `-a`

If specified, will set the newly registered module as default version.

#### Examples

```bash
# Register from a local path
module register /path/to/module/package
# Register from a zip file, and set as default version when registered
module register /path/to/module_package.zip --set-as-default-version
# For the case contains multiple spec files in the module package
module register /path/to/module_package_which_contains_multiple_specs.zip --spec-file=my_favourite_module_spec.yaml
# Register from GitHub
module register https://github.com/zzn2/sample_modules/tree/master/one_spec
module register https://github.com/zzn2/sample_modules/tree/master/multiple_specs_subfolder --spec-file=spec/clean_missing_data.yaml
```



### module list

Lists the modules in the workspace.

Will show the following information about the module:

* Name
* Default version
* Description
* Last modified date

```bash
module list [--include-builtin-modules]
```

##### `--include-builtin-modules` `-a`
If specified, will list the built-in modules.
> This field is optional. If not specified, defaults to `False`.

#### Examples

```bash
# Show as table
module list --output=table
# Show as table, including the built-in modules
module list -a --output=table
```



### module show

Shows detail information of a given module.

* Use `--output table` will show the same information with `module list`.
* Use `--output json` will show more detailed information such as module ports, parameters, etc.

```bash
module show --name
           [--version]
```

##### `--name`
Specify the name of the module to be shown.

##### `--version`
Specify the module version.
> This field is optional. If not specified, the default version will be shown.

#### Examples

```bash
# Show detailed information, including name, version, interfaces, etc.
module show --name="My Awesome Module"
# Show the detailed information for a specific version.
module show --name="My Awesome Module" --version=0.0.1
# Show full schema for a module.
module show --name="My Awesome Module" --verbose
```



### module set-default-version

Sets a default version for a module.

```bash
module set-default-version --name
                           --version
```

##### `--name`
Specify the name of the module.

##### `--version`
Specify the module version to be set as default.

#### Examples

```bash
module set-as-default-version --name="My Awesome Module" --version=0.0.100
```



### module disable

Disable a module.

```bash
module disable --name
```

##### `--name`
Specify the name of the module.

#### Examples

```bash
module disable --name="My not-so-Awesome Module"
```



### module enable

Enable a module.

```bash
module disable --name
```

##### `--name`

Specify the name of the module.

#### Examples

```bash
module enable --name="My Awesome Module"
```



### module download

Downloads a module spec and snapshot to a local folder. The downloaded folder can be used to register as a module to other workspaces.
```bash
module download --name
               [--version]
               [--target-dir]
               [--overwrite]
```
##### `--name`
Specify the name of the module to be downloaded.

##### `--version`
Specify the module version. If not specified, will download the default version.
##### `--target-dir` `-t`
Specify the target directory to save the module package to. If not specified, use the current working directory.

##### `--overwrite` `-y`

Overwrite if the target directory not empty. If not specifid, will prompt whether to overwrite.

#### Examples

```bash
# Download module default version to the current directory
module download --name="My Awesome Module"
# Download specific version of module
module download --name="My Awesome Module" --version=0.0.100
# Specify the target directory
module download --name="My Awesome Module" --target-dir=/path/to/dir --overwrite
```

