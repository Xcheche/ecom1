# Generating ERDs with django-extensions

`django-extensions` can generate an Entity Relationship Diagram (ERD) of your Django models using the `graph_models` management command.

## 1. Install django-extensions

```bash
pip install django-extensions
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_extensions',
]
```

## 2. Install Graphviz

`graph_models` depends on Graphviz.

### Ubuntu/Debian

```bash
sudo apt-get install graphviz graphviz-dev
```

### macOS

```bash
brew install graphviz
```

### Windows

Download and install Graphviz from:

https://graphviz.org/download/

Verify installation:

```bash
dot -V
```

Expected output:

```bash
dot - graphviz version 12.x.x
```

## 3. Generate an ERD for a Specific App

```bash
python manage.py graph_models myapp -o erd.png
```

Example:

```bash
python manage.py graph_models accounts -o accounts_erd.png
```

## 4. Generate an ERD for All Apps

```bash
python manage.py graph_models -a -o project_erd.png
```

Where:

- `-a` = all installed apps
- `-o` = output file

## 5. Generate a DOT File

```bash
python manage.py graph_models -a > project.dot
```

Then render manually:

```bash
dot -Tpng project.dot -o project_erd.png
```

Other formats:

```bash
dot -Tpdf project.dot -o project_erd.pdf
dot -Tsvg project.dot -o project_erd.svg
```

## 6. Useful Options

### Show Inheritance

```bash
python manage.py graph_models -a --inheritance -o erd.png
```

### Group Models by App

```bash
python manage.py graph_models -a --group-models -o erd.png
```

### Include Fields

```bash
python manage.py graph_models -a --fields -o erd.png
```

### Exclude Apps

```bash
python manage.py graph_models -a \
    -X admin,auth,sessions,contenttypes \
    -o erd.png
```

## 7. Example

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )

class Category(models.Model):
    name = models.CharField(max_length=100)

class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
```

Running:

```bash
python manage.py graph_models library --fields -o library_erd.png
```

Produces a diagram showing:

- `Author` → `Book` (one-to-many)
- `Book` → `BookCategory`
- `Category` → `BookCategory`

## 8. Common Issues

### CommandError: Neither pygraphviz nor pydotplus could be found

```bash
pip install pygraphviz
```

or

```bash
pip install pydotplus
```

**Note**: `pygraphviz` has been installed in the virtual environment to resolve this issue.

### dot executable not found

Graphviz is not installed or not in your PATH.

Check:

```bash
which dot
```

or on Windows:

```cmd
where dot
```

## Recommended Command

```bash
python manage.py graph_models -a \
    --group-models \
    --fields \
    --inheritance \
    -o erd.png
```

This generates a comprehensive ERD with model fields, relationships, inheritance hierarchies, and app grouping.
