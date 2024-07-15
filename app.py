from flask import Flask, render_template, request
from utils.kabum import scrape_kabum
from utils.terabyteshop import scrape_terabyteshop
import concurrent.futures

app = Flask(__name__)


def price_to_float(price_str):
    """
    Converte um preço em formato string para float.
    Exemplo: 'R$ 1.234,56' -> 1234.56
    """
    try:
        if price_str:
            price_str = price_str.replace('R$', '').replace(
                '.', '').replace(',', '.').strip()
            return float(price_str)
    except ValueError as e:
        print(f"Erro ao converter preço para float: {price_str} - {e}")
    return 0.0  # Retorna 0.0 se a conversão falhar


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    products = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_kabum = executor.submit(scrape_kabum, query)
                future_terabyteshop = executor.submit(
                    scrape_terabyteshop, query)

                kabum_results = future_kabum.result()
                terabyteshop_results = future_terabyteshop.result()

                products.extend(kabum_results)
                products.extend(terabyteshop_results)

            # Ordena a lista de produtos pelo preço
            products.sort(key=lambda x: price_to_float(x['price']))

    return render_template("index.html", products=products, query=query)


if __name__ == '__main__':
    app.run(debug=True)
