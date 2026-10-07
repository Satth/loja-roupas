from loja.carrinho import Carrinho
from loja.produto import Produto

class BlackFriday:
    def aplicar_desconto(self, subtotal): # nome errado
        return subtotal * 0.5
    
c = Carrinho(BlackFriday())
c.adicionar(Produto("Moletom", 159.90, "P"))
print("carrinho montado")   # aparece
print(c.total)