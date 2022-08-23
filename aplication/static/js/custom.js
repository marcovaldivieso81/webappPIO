// APIREST PRODUCTOS
//
fetch('/ventas/api_productos').then(response => response.json()).then(data=>{
	lista_productos=data
	new Autocomplete(document.getElementById('pname'), {
		data: lista_productos.products,
		onSelectItem: ({ value}) => {
		//console.log("user selected:", label, value);
		document.getElementById('pname').dataset.value=value
		}
	});
}).catch(err=>console.log(err))
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
// ACTUALIZA FECHAS DEL INPUT PRINCIPAL
document.addEventListener("input",(event) => {
    if(!["FechaInicial", "FechaFinal"].includes(event.target.id)){return}
    if (ValidarFechas("FechaInicial","FechaFinal")){
        document.getElementById('alerta1').hidden = true
        return}
    StartFecha("FechaInicial","FechaFinal")
    document.getElementById('alerta1').hidden = false
});
// ACTUALIZA FECHAS DEL INPUT SINC
document.addEventListener("input",(event) => {
    if(!["FechaInicialSinc", "FechaFinalSinc"].includes(event.target.id)){return}
    if (ValidarFechas("FechaInicialSinc","FechaFinalSinc")){
        document.getElementById('alerta2').hidden = true
        return}
    StartFecha("FechaInicialSinc","FechaFinalSinc")
    document.getElementById('alerta2').hidden = false
});

// INICIA FECHA DEFAULT DEL FORMULARIO
//
StartFecha("FechaInicial","FechaFinal")
StartFecha("FechaInicialSinc","FechaFinalSinc")
// 
function FillExport(){
    form=document.getElementById('ExportForm')
    form.querySelector('div').replaceChildren()
    for(row of document.getElementById('filastabla').children){
        if (!row.hidden){
            input=document.createElement('input')
            input.name='pedidos'
            input.value=row.id
            form.querySelector('div').append(input)
        }
    }
}
// BUSQUEDA POR AUTOCOMPLETADO
//
document.getElementById('buscar').addEventListener('input',(event)=>{
    buscando=event.target.value.toLowerCase()
    for(let fila of document.getElementById('filastabla').children){
        texto=fila.children[5].innerText.toLowerCase()
        fila.hidden=!texto.includes(buscando)
    }
    FillExport()
})

FillExport()
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
//
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
		// CONSULTA DE DATOS DEL PRODUCTO
        selectedRow=seleccion.id
		fetch('/ventas/api_productos?idpedido='+selectedRow)
			.then(response => response.json())
			.then(data=>{
			datos_pedido=data

			document.getElementById('pedido-id').value=selectedRow
			document.getElementById('pedido-notas').value=datos_pedido.Notas
			document.getElementById('pedido-observacion').value=datos_pedido.Observacion
			document.getElementById('pedido-nombrecliente').value=datos_pedido.NombreCliente
			document.getElementById('pedido-telefono').value=datos_pedido.Telefono
			document.getElementById('pedido-direccion').value=datos_pedido.Direccion
			document.getElementById('pedido-fechahora').value=datos_pedido.FechaHora
			document.getElementById('pedido-cancelado').checked=datos_pedido.Cancelado
			document.getElementById('pedido-servicios').checked=datos_pedido.Servicio
            document.getElementById('confirmed-by-customer').checked=datos_pedido.Confirmed_by_customer
            document.getElementById('in-production').checked=datos_pedido.In_Production


			/*for(let servicio of document.getElementById('pedido-servicios').children){
				if(servicio.value == datos_pedido.Servicio){
					servicio.selected=true
				}
				}*/
			for(let estado of document.getElementById('pedido-estados').children){
				if(estado.value == datos_pedido.Estado){
					estado.selected=true
				}
				}

			tbody=document.querySelector("#example tbody")
            //console.log(tbody.classList.contains('lectura'))
			tbody.replaceChildren()
                if(!tbody.classList.contains('lectura')){
                    for({cantidad:quantity,variante_id__IdArticulo__Descripcion:variante,variante_id__Descripcion:desc,variante_id:id} of datos_pedido.ListaPedidos){
					tbody.append(productRow(variante+ ' - ' + desc, id, quantity))                      }
                }else{
                     for({cantidad:quantity,variante_id__IdArticulo__Descripcion:variante,variante_id__Descripcion:desc} of datos_pedido.ListaPedidos){
					tbody.append(productRowLectura(variante+ ' - ' + desc, quantity))
                    } 
                }
            })
			.catch(err=>console.log(err))
    })
})
//	CONTRUYE ROW DE PRODUCTO LECTURA DESDE TEMPLATE
//
rowTemplateLectura = document.getElementById('template-prod-lectura').content
function productRowLectura(name,quantity){
	row=rowTemplateLectura.cloneNode(true)
	row.querySelector('.pname-td').innerText=name
	row.querySelector('.pquantity-td').innerText=quantity
	return row
}
//	CONTRUYE ROW DE PRODUCTO DESDE TEMPLATE
//
rowTemplate = document.getElementById('template-prod').content
function productRow(name,id,quantity){
	row=rowTemplate.cloneNode(true)
	row.querySelector('.pname-td').innerText=name
	row.querySelector('.pquantity-td').innerText=quantity
	row.querySelector('input').value=JSON.stringify({name:id, quantity})
	return row
}

tbody=document.querySelector("#example tbody")
if(!tbody.classList.contains('lectura')){
// ANADE ROW PRODUCTO A LA TABLA
    document.getElementById('addBtn').addEventListener('click',function(){
	    var id=document.getElementById('pname').dataset.value
        var name = document.getElementById('pname').value;
        var quantity = document.getElementById('pquantity').value;
	    if(id==null || quantity ==''){return}
	    delete document.getElementById('pname').dataset.value
	    document.getElementById('pname').value = ''
        document.getElementById('pquantity').value = '1'
        document.querySelector("#example tbody").append(productRow(name, id, quantity));
    });
//ELIMINA ROW PRODUCTO AL HACER CLICK EN ICONO PAPELERA    
    document.getElementById('example').addEventListener("click", function (event) {
        if(!event.target.matches('.delBtn')){return}
        event.target.closest('tr').remove()
    });
}

//EXPORTAR A EXCEL
//
/*
$("#table-products").table2excel({
//    exclude: ".excludeThisClass",
    name: "Worksheet Name",
    filename: "SomeFile.xls", // do include extension
    preserveColors: false // set to true if you want background colors and font colors preserved
});
*/
