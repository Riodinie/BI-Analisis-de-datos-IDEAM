function ejecuta() {

    let boton_1= document.getElementById("w-tabs-0-data-w-tab-0");
    let boton_2= document.getElementById("w-tabs-0-data-w-tab-1");
    boton_1.addEventListener('click',text_1)
    boton_2.addEventListener('click',text_2)
    
    }
    
    function text_1() {

    document.getElementById("Primero").style.display = "block";
    document.getElementById("Segundo").style.display = "none";


    this.classList.add('w--current');
      // Remover la clase 'w--current' del otro botón si está presente
      let boton_2 = document.getElementById("w-tabs-0-data-w-tab-1");
      boton_2.classList.remove('w--current');
    
    
    }
    
    function text_2() {
        
    document.getElementById("Segundo").style.display = "block";
    document.getElementById("Primero").style.display = "none";


    this.classList.add('w--current');
      // Remover la clase 'w--current' del otro botón si está presente
      let boton_1 = document.getElementById("w-tabs-0-data-w-tab-0");
      boton_1.classList.remove('w--current');
    }
    
    
    
    window.addEventListener("load",ejecuta,false);
    
    