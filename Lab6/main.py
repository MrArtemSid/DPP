import cherrypy
from peewee import *

db = PostgresqlDatabase(None)


def init():
    db.init("db", host="127.0.0.1", user="sid_key", password="1")
    db.connect()
    db.create_tables([Products])


class Products(Model):
    id = AutoField()
    name = CharField()
    cnt = IntegerField()
    price = DoubleField()

    class Meta:
        database = db


def html_alert(string):
    return f"""
            <script>
                alert('{string}');
                window.location.href = '/';
            </script>
                """


def html_table_tr(var_name):
    item_style = """style='border: 1px solid black;'"""
    return f"""<th {item_style}>{var_name}</th>"""


def html_of_table():
    table_html = f"""
            <table style='border-collapse: collapse;'>
                <tr>
                    {html_table_tr("id")}
                    {html_table_tr("Name")}
                    {html_table_tr("Price")}
                    {html_table_tr("Amount")}
                </tr>"""
    for product in Products.select():
        table_html += f"""
                <tr>
                    {html_table_tr(product.id)}
                    {html_table_tr(product.name)}
                    {html_table_tr(product.price)}
                    {html_table_tr(product.cnt)}
                </tr>"""
    table_html += """</table>"""

    return table_html


def html_select_ids():
    ans = []
    for product in Products:
        ans.append(f"""<option value="{product.id}">{product.id}</option>""")
    return "\n".join(ans)


def html_datalists():
    res = ""
    ans = dict()
    ans["names"] = ["""<datalist id="names">"""]
    ans["ids"] = ["""<datalist id="ids">"""]
    ans["prices"] = ["""<datalist id="prices">"""]
    ans["cnts"] = ["""<datalist id="cnts">"""]
    for product in Products:
        ans["names"].append(f"""<option value="{product.name}">{product.name}</option>""")
        ans["ids"].append(f"""<option value="{product.id}">{product.id}</option>""")
        ans["prices"].append(f"""<option value="{product.price}">{product.price}</option>""")
        ans["cnts"].append(f"""<option value="{product.cnt}">{product.cnt}</option>""")
    for var in ["names", "cnts", "ids", "prices"]:
        ans[var].append("""</datalist>""")
        res += "\n".join(ans[var])
    return res


def html_style():
    return """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 4px;
            text-align: left;
        }
    </style>"""


def handle_products():
    html = f"""
            <form method="post">
                <select name="id">
                    {html_select_ids()}
                </select>
                {html_datalists()}
                <input type="text" list="names" name="name" placeholder="Product Name">
                <input type="number" list="prices" name="price" placeholder="Price">
                <input type="number" list="cnts" name="cnt" placeholder="Amount"><br>
                <button type="submit" onclick="javascript: form.action='/add_product';">Add Product</button>
                <button type="submit" onclick="javascript: form.action='/delete_product';">Delete Product</button>
                <button type="submit" onclick="javascript: form.action='/update_product';">Update Product</button>
            </form>"""
    return html


class Main(object):
    @cherrypy.expose
    def index(self):
        return f"""<html>
          <head>
          {html_style()}
          </head>
          <body>
            {html_of_table()}<br>
            {handle_products()}
          </body>
        </html>"""

    @cherrypy.expose
    def add_product(self, id=None, name=None, price=None, cnt=None):
        buf = ''

        if len({name, price, cnt} & {'', None}) > 0:
            buf = 'Item was not added. Check the input'
        else:
            buf = f'{name} was successfully added'
            Products.create(name=name, price=price, cnt=cnt)

        return html_alert(buf)

    @cherrypy.expose
    def delete_product(self, id=None, name=None, price=None, cnt=None):
        if not Products.get_or_none():
            return html_alert("There is nothing to delete")
        name = Products.get_by_id(id).name
        Products.delete_by_id(id)
        return html_alert(f'{name} (id = {id}) was successfully deleted')

    @cherrypy.expose
    def update_product(self, id=None, name=None, price=None, cnt=None):
        if not Products.get_or_none():
            return html_alert("There is nothing to update")

        buf = ''
        if len({id, name, price, cnt} & {'', None}) > 0:
            buf = 'Item was not updated. Check the input'
        else:
            product = Products.get_by_id(id)
            product.name = name
            product.price = price
            product.cnt = cnt
            product.save()
            buf = f'Product with ID {id} has been successfully updated'

        return html_alert(buf)


def main():
    init()
    cherrypy.quickstart(Main())


main()
