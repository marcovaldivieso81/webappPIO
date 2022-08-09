// VALIDA SI UNA FECHA ES MAYOR QUE OTRA
function ValidarFechas(IdInicio,IdFin){
    var fechainicial = document.getElementById(IdInicio).value;
    var fechafinal = document.getElementById(IdFin).value;
    if(fechafinal < fechainicial) {
        return false
    }else{
        return true
    }
}
// SUMA UN NÚMERO DE DIAS DETERMINADO A UNA FECHA
function SumaDias(Fecha,dias){
    var nuevafecha = new Date(Fecha.setDate(Fecha.getDate() + dias))
    return nuevafecha
}
// INICIALIZA FECHAS
function StartFecha(IdInicio,IdFin){
    params=new URLSearchParams(location.search)
    offset = new Date().getTimezoneOffset()
    FechaActual = new Date() 
    if(params.get('initial')==null){
        FechaActualF = Date.parse(FechaActual.toString()) - (offset * 60 * 1000)
        FechaActualF = new Date(FechaActualF).toISOString().slice(0,10)
    }else{
        FechaActualF=params.get('initial')
    }
    document.getElementById(IdInicio).value = FechaActualF;   
    FechaFin = SumaDias(FechaActual, 1)
    if(params.get('final')==null){
        FechaFinF = Date.parse(FechaFin.toString()) - (offset * 60 * 1000)
        FechaFinF = new Date(FechaFinF).toISOString().slice(0,10)
    }else{
        FechaFinF=params.get('final')
    }
    document.getElementById(IdFin).value = FechaFinF;
}
// ACTUALIZA FECHAS DE LOS INPUT LUEGO DEL SINC
document.addEventListener("input",(event) => {
    if(!["FechaInicial", "FechaFinal"].includes(event.target.id)){return}
    if (ValidarFechas("FechaInicial","FechaFinal")){
        document.getElementById('alerta1').hidden = true
        return}
    StartFecha("FechaInicial","FechaFinal")
    document.getElementById('alerta1').hidden = false
});

StartFecha("FechaInicial","FechaFinal")
StartFecha("FechaInicialSinc","FechaFinalSinc")

// BUSQUEDA POR AUTOCOMPLETADO
//
document.getElementById('buscar').addEventListener('input',(event)=>{
    buscando=event.target.value.toLowerCase()
    for(let fila of document.getElementById('filastabla').children){
        texto=fila.children[5].innerText.toLowerCase()
        fila.hidden=!texto.includes(buscando)
    }
})

// COLOREADO FECHA ACTUAL
//
for(let fila of document.getElementById('filastabla').children){
    contentFila = fila.children[0].children[0]
    FechaFila = contentFila.innerHTML.split('-')
    FechaFila = new Date(FechaFila[2],FechaFila[1]-1,FechaFila[0])
    FechaActual = new Date()
    if(FechaActual.toDateString()==FechaFila.toDateString()){
        contentFila.style.backgroundColor = "#40E0D0"       
    }
}

//SELECCIONA UNA FILA DE UNA TABLA
var selectedRow = null
Filas=document.querySelectorAll('[name="rowtable"]')
Filas.forEach((fila) => {
    fila.addEventListener('click',(event)=>{
        filaspintadas=document.querySelectorAll('.bg-yellow')
        filaspintadas.forEach((filapintada) =>{
            if(filapintada){
                filapintada.classList.remove('bg-yellow')
            }
        })
        seleccion=event.currentTarget
        seleccion.classList.add('bg-yellow')
        selectedRow=seleccion.id
    })
})

// ADD PRODUCT
//
document.getElementById('addBtn').addEventListener('click',function(){
    var name = document.getElementById('pname').value;
    document.getElementById('pname').value = ''
    var addr = document.getElementById('pquantity').value;
    document.getElementById('pquantity').value = ''
    var markup = "<tr><td>" + name + "</td><td>" + addr + "</td><td><button class='btn btn-small btn-danger delBtn'> <i class='bi bi-trash delBtn'></i> </button></td></tr>";
    document.querySelector("#example tbody").innerHTML+=markup;
    });
    
document.getElementById('example').addEventListener("click", function (event) {
    if(!event.target.matches('.delBtn')){return}
    event.target.closest('tr').remove()
});

