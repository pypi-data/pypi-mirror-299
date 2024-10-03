# Whiteduck Project Scaffolding Tool

A tool to scaffold python projects with Whiteduck's recommended tech stack.


## Installation

```bash
pip install whiteduck
```

update

```bash
pip install -U whiteduck
```

## Commands

### Wizard

Run without any parameter

```bash
whiteduck
```

### Create a New Project

```bash
whiteduck create [--template TEMPLATE_NAME] [--output OUTPUT_PATH]
```

`--template` (optional): The name of the template to use. Defaults to the default template.

`--output` (optional): The output path for the new project. Defaults to the current directory.


### List Available Templates

```bash
whiteduck list-templates
```

### Display Template Information

```bash
whiteduck template-info TEMPLATE_NAME
```



