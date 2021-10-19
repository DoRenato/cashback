Sobre a API:

Utilizando o Django Rest Framework, tentei fazer o mais parecido possível com as sugestões propostas. Portanto, basta acessar o link "http://localhost:8000/api/cashback/", onde: <br>
    * Ao utilizar o método GET ela apresenta todos os cashback's que foram salvos com sucesso, da mesma forma do exemplo apresentado.
    * Já o POST, também procurei deixar fiel ao exemplo, portanto basta enviar um json no modelo do fluxograma de exemplo que a API irá validar todos os dados.
    
      OBS: O fluxograma do exemplo estava dando erro pois continha virgulas sem conteúdos posteriores, ex:

        "customer": {
            "document": "00000000000",    |Essa virgula seguida de um fechamento da chave causa um erro de interpretação do JSON (pelo menos utilizando o django rest),
            "name": "JOSE DA SILVA",  <-- |mas bastou removê-las que funcionou normalmente, são 4 no total que estão dessa forma.
         },

Etapas da validação:

1- Ao receber a requisição, a API verifica primeiro se o cliente já está cadastrado no sistema, senão, verifica se CPF do usuário é válido, se for, o cliente é cadastrado no sitema através da app 'users' onde contem em 'models.py' o modelo para salvar novos clientes.
    * A validação do CPF se dá através do arquivo 'validations.py' localizado em '/sales/api/validations.py', onde o mesmo contem todos os passos necessários para a validação do mesmo.

2- Logo em seguida, após o cliente salvo, irá verificar se o formato da data/hora estão corretas. Como a data será salva em um modelo DateTimeField, se o formato não estiver de acordo, então não salva. Caso esteja tudo certo com a data/hora, a API irá registrar um novo modelo no banco entitulado 'Cashback' onde o mesmo armazena todos os dados necessários que foram recebidos através da requisição, incluindo um campo adicional onde fica salvo o valor total do cashback.

3- Com a data/hora válidas, a próxima etapa do processo é validar produtos. É feito um laço 'for' para percorrer todos os produtos que foram recebidos, onde irão passar pelas seguintes etapas: 

    - TIPO: irá verificar se o tipo do produto condiz com os tipos que estão elegíveis para a promoção de cashback. Como padrão, criei um modelo no banco
      onde ficam armazenados os tipos de produtos aceitos e o cashback que cada um gera (Achei melhor dividir o cashback por tipo do produto e depois somar
      cada cashback do tipo pra gerar o valor total de cashback). Ao iniciar o laço, a API compara se o tipo do produto da vez está
      cadastrado no banco. Caso não esteja, a API irá ignorar o mesmo e passar para o próximo da sequência. Portanto, se uma compra tiver 3 produtos mas
      apenas um tipo for aceito, será salvo e gerado o cashback somente daquele produto aceito. Este procedimento também serve paraO mesmo processo
      acontece para os casos de erros que serão apresentados posteiormente.

  - VALOR e QUANTIDADE: Após a verificação do tipo, a API irá verificar se a quantidade e os valoresquantidade são válidos. Essa validação é feita
    Comparando se o valor do produto é menor ou igual a 00,00 ou então se a quantidade é menor ou igual a zero. Se algum desses casos for verdade,
    a API irá ignorar o produto da vez e passar para o proximo da sequência.
      
4- Estando válido um produto, o calculo é feito de forma bem simples, onde será multiplicado o valor do produto pela quantidade adquirida, e esse
    valor vai sendo armazenado em uma variável 't' que vai sendo incrementada a cada nova soma de produto. O cashback é gerado pelo mesmo calculo
    com a adição de uma multiplicação no final onde seria a quantidade multiplicada pelo valor do produto, e esse resultado é multiplicado pelo valor
    do cashback do tipo do produto divido por 100 - ((valor * quantidade) * (cashback/100)) - e esse valor também é armazenado em uma variavel de
    incremento 'cashback'. Ao final de todo o laço, 't' terá a soma total de todos os produtos e 'cashback' o Cashback gerado. Como na requisição é
    informado o valor total da compra, esse mesmo valor é comparado ao armazenado em 't'. Se ambos forem iguais, tudo fica salvo no banco e vamos para a
    etapa final, caso contrário, todo o processo é descartado e apagado do banco.

5- Com todos as validações aprovadas, utilizando a biblioteca 'requests' (instalada através do pip), é feita a requisição para a API externa onde são
enviados o documento do cliente e o cashback gerado. Pelos testes a API externa retornou exatamente igual ao do exemplo apresentado.

Houve algumas validações que achei pertinente adicionar e que não constavam na proposta, que seriam os casos em que os valores do produto ou a quantidade
fossem menores ou igual a 0(zero), onde a api não iria computar, assim indo para o produto posterior. Caso o total da compra também for igual a 0(zero), os dados
serão descartados, visando salvar somente vendas ondem tenha no mínimo um valor total de 00,01.



Como executar:

Projetei o banco para a API ir buscar nos modelos o json na mesma forma do exemplo apresentado. Portanto, a App sales.Sale é responsável por retornar a venda por completo - produtos, tipo, total, cliente

Não quis deixar o Tipo com valores fixos pois pensei que um tipo poderia variar de valor, ex: tipo A seria feijão, e existem marcas diferentes, com valores diferentes. Assim, só o cashback desse tipo que é fixo.