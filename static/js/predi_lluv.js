function ejecuta() {

    let boton_1= document.getElementById("w-tabs-0-data-w-tab-0");
    let boton_2= document.getElementById("w-tabs-0-data-w-tab-1");
    boton_1.addEventListener('click',text_1)
    boton_2.addEventListener('click',text_2)
    
    }
    
    function text_1() {

    document.getElementById("Primero").style.display = "block";
    document.getElementById("Segundo").style.display = "none";


    this.setAttribute('aria-selected', 'true');
      // Remover la clase 'w--current' del otro botón si está presente
      let boton_2 = document.getElementById("w-tabs-0-data-w-tab-1");
      boton_2.removeAttribute('aria-selected');
    
    
    }
    
    function text_2() {
        
    document.getElementById("Segundo").style.display = "block";
    document.getElementById("Primero").style.display = "none";


    this.setAttribute('aria-selected', 'true');
      // Remover la clase 'w--current' del otro botón si está presente
      let boton_1 = document.getElementById("w-tabs-0-data-w-tab-0");
      boton_1.removeAttribute('aria-selected');
    }
    
    
    
    window.addEventListener("load",ejecuta,false);
    
    