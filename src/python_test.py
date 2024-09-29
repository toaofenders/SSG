from markdown_htmlnode import *
# Import necessary modules here

def main():
# Your code goes here
    text = """
# My Favorite Foods

Here's a list of my top 3 favorite foods:

1. Pizza
2. Ice Cream
3. Sushi

## Why I Love Pizza

Pizza is **amazing** because:

* It's customizable
* It's perfect for sharing
* It's delicious hot *or* cold

Here's a quote about pizza:

> Pizza is like the entire food pyramid!

And here's some code to order pizza:

```python
def order_pizza():
    print("One large pepperoni pizza, please!")"""
    print(text)
    print(markdown_to_html_node(text))
    




# This condition checks if the script is being run directly
# and not being imported as a module in another script.
if __name__ == "__main__":
    main()

