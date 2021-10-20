# Sobre a API:

## Requisitos e Execução

- É recomendável utilizar um ambiente virtual para instalar os requisitos, todos os necessários estão no arquivo requirements.txt
- Na pasta raiz do projeto, execute o comando **python manage.py migrate** para criar o banco.
- Crie um super usuário para cadastrar os tipos de produtos no banco para validar o Cashback:
  * Na pasta raiz do projeto, execute o *manage.py* pelo terminal da seguinte forma: **python manage.py createsuperuser**  
    coloque os dados e então vá para página de Administração do Django (http://localhost:8000/admin/) e faça login com o super usuário.  
  * Estando logado, cadastre os tipos em 'Product Types' - A API so irá validar se os tipos forem um dos três (A, B ou C), então, embora que cadastre mais tipos, ela só irá validar estes.
- Feito isso, a API já está pronta para funcionar. 

## Overview

Utilizando o Django Rest Framework, tentei fazer o mais parecido possível com as sugestões propostas. Portanto, basta acessar o link "http://localhost:8000/api/cashback/", onde:  
- Ao utilizar o método GET ela apresenta todos os cashback's que foram salvos com sucesso.  
- Já o POST, procurei deixar fiel ao exemplo, portanto basta enviar um json no modelo do fluxograma de exemplo que a API irá validar todos os dados.  
  * OBS: O fluxograma do exemplo estava dando erro pois continha virgulas sem conteúdos posteriores, ex:

        "customer": {
            "document": "00000000000",    |Essa virgula seguida de um fechamento da chave causa um erro de interpretação do JSON (pelo menos utilizando o django rest),
            "name": "JOSE DA SILVA",  <-- |mas bastou removê-las que funcionou normalmente, são 4 no total que estão dessa forma.
         },

## Etapas da validação:

1- Ao receber a requisição, a API verifica primeiro se o cliente já está cadastrado no sistema, senão, verifica se CPF do usuário é válido, se for, o cliente é cadastrado no sitema através da app 'users' onde contem em 'models.py' o modelo para salvar novos clientes.  
- A validação do CPF se dá através do arquivo 'validations.py' localizado em '/sales/api/validations.py', onde o mesmo contem todos os passos necessários para a validação do CPF.

2- Logo em seguida, após o cliente salvo, irá verificar se o formato da data/hora estão corretas. Como a data será salva em um modelo DateTimeField, se o formato não estiver de acordo, então não salva. Caso esteja tudo certo com a data/hora, a API irá registrar um novo modelo no banco entitulado 'Cashback' onde o mesmo armazena todos os dados necessários que foram recebidos através da requisição, incluindo um campo adicional onde fica salvo o valor total do cashback.

3- Com a data/hora válidas, a próxima etapa do processo é validar produtos. É feito um laço 'for' para percorrer todos os produtos que foram recebidos, onde irão passar pelas seguintes etapas: 

- TIPO: irá verificar se o tipo do produto condiz com os tipos que estão elegíveis para a promoção de cashback. Como padrão, criei um modelo no banco onde ficam armazenados os tipos de produtos aceitos e o cashback que cada um gera (Achei melhor dividir o cashback por tipo do produto e depois somar cada cashback do tipo pra gerar o valor total de cashback). Ao iniciar o laço, a API compara se o tipo do produto da vez está cadastrado no banco. Caso não esteja, a API irá ignorar o mesmo e passar para o próximo da sequência. Portanto, se uma compra tiver 3 produtos mas apenas um tipo for aceito, será salvo e gerado o cashback somente daquele produto aceito. Este procedimento também serve paraO mesmo processo acontece para os casos de erros que serão apresentados posteiormente.  

- VALOR e QUANTIDADE: Após a verificação do tipo, a API irá verificar se a quantidade e os valoresquantidade são válidos. Essa validação é feita Comparando se o valor do produto é menor ou igual a 00,00 ou então se a quantidade é menor ou igual a zero. Se algum desses casos for verdade, a API irá ignorar o produto da vez e passar para o proximo da sequência.
      
4- Estando válido um produto, o calculo é feito de forma bem simples, onde será multiplicado o valor do produto pela quantidade adquirida, e esse valor vai sendo armazenado em uma variável 't' que vai sendo incrementada a cada nova soma de produto.  

O cashback é gerado pelo mesmo calculo com a adição de uma multiplicação no final onde seria a quantidade multiplicada pelo valor do produto, e esse resultado é multiplicado pelo valor do cashback do tipo do produto divido por 100  
- ((valor * quantidade) * (cashback_do_tipo/100))  

e esse valor também é armazenado em uma variavel de incremento 'cashback'. Ao final de todo o laço, 't' terá a soma total de todos os produtos e 'cashback' o Cashback gerado. Como na requisição é informado o valor total da compra, esse mesmo valor é comparado ao armazenado em 't'. Se ambos forem iguais, tudo fica salvo no banco e vamos para a etapa final, caso contrário, todo o processo é descartado e apagado do banco.

5- Com todos as validações aprovadas, utilizando a biblioteca 'requests' (instalada através do pip, serve para fazer requisições à API's, por exemplo.), é feita a requisição para a API externa onde são enviados o documento do cliente e o cashback gerado. Pelos testes a API externa retornou exatamente igual ao do exemplo apresentado.

6- Sobre autenticação, no repositório já deixei o banco 'db.sqlite3' disponível para ter acesso direto, mas caso prefira iniciar um novo
banco do zero, a forma de autenticação se dá no seguinte:
- Cadastre um novo usuario no sistema: http://localhost:8000/users/register
- Após isso, acesse http://localhost:8000/api-token-auth/ e envie através do método POST seu usuario e senha que você cadastrou, no seguinte formato:  

{
    "username":"seu_usuario",
    "password":"sua_senha"
}  

A API irá retornar seu token de acesso. Após isso, utilizando o Postman (https://www.postman.com/home) basta adicionar na aba 'Headres' os seguintes valores:
- na coluna 'key': Authorization.
- na coluna 'value': Token 123 (substitua '123' pelo token de acesso gerado) 

Com o Header já adicionado, agora só precisa ir para a aba 'Body' que fica ao lado da aba 'Headers', onde nela irá enviar o JSON com os dados necessarios para validação na API (os do exemplo do fluxograma 1). Estando em 'Body', basta clicar em 'raw' e selecionar o tipo 'JSON' (por padrão vai estar TEXT, esse tipo fica na mesma linha do 'raw', é a ultima opção seguindo para a direita, destacado na cor azul). Com esse procedimento feito, não deve ocorrer problema algum e a API irá retornar a seguinte mensagem: "Cashback generated."

Acredito que consegui explicar o necessário, qualquer nova informação incremento aqui :D . 