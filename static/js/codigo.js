let seccion=document.querySelector(".seccion");
let rayitas=document.querySelector("#rayas");
document.querySelector("#cerrar").addEventListener("click",()=>(closeNav()));
rayitas.addEventListener("click",()=>openNav());
rayitas.style.cursor="pointer";

seccion.addEventListener("click",()=>{

    closeNav();
    

})

let abierto=false;
const openNav=()=>
{
    if (abierto)
    {
        return closeNav();
    }else
    {
        try 
        {
            abierto=true;    
            document.getElementById("sideNavigation").style.width = "250px";
            document.getElementById("main").style.marginLeft = "250px";
        } catch(e) 
        {}
    }
}
             
const closeNav=()=>
{
    try 
    {                
    abierto=false;
    document.getElementById("sideNavigation").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    } catch(e) 
    {}
}
