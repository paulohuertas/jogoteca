$('form input[type="file"]').change(event => {
  let arquivos = event.target.files;
  if (arquivos.length === 0) {
    console.log('sem imagem pra mostrar')
  } else {
      if(arquivos[0].type == 'image/jpeg') {
        $('img').remove();
        let imagem = $('<img class="img-responsive">');
        imagem.attr('src', window.URL.createObjectURL(arquivos[0]));
        $('figure').prepend(imagem);
      } else {
        alert('Formato não suportado')
      }
  }
});


/* function alterarImagem(){
        var attachFile = document.getElementsByTagName('input')[0];
        let imgOriginal = document.getElementsByTagName('img')[0];
        attachFile.addEventListener('change', (event) => {
        let listOfFiles = event.target.files;
        if (listOfFiles.length == 0){
            console.log("nao ha nenhum arquivo selecionado");
        } else {
            if (listOfFiles[0].type == "image/jpeg"){
                imgOriginal.remove();
                let imagem = document.createElement('img');
                imagem.setAttribute('class', 'img-responsive');
                imagem.setAttribute('src', window.URL.createObjectURL(listOfFiles[0]));
                let figure = document.getElementsByTagName('figure')[0].prepend(imagem);
                //figure.prepend(imagem);
                i++;
            } else{
                alert("Tipo de arquivo nao suportado");
            }
        }
    });
}
*/