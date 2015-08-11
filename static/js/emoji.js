/**
 * Created by py on 1/22/15.
 */
function addemoji(emoji){
    var a = document.getElementById('content').value;
    //a = a+'<img class="emoji_img" src="/static/emoji/img/cat.png"/>';
    a = a+':'+emoji+':'
    document.getElementById('content').value=a;
}

function show_emoji(){
    if(document.getElementById("emoji_list").style.display == "inline")
        {
            document.getElementById("emoji_list").style.display ="none";
        }
    else
        {
             document.getElementById("emoji_list").style.display = "inline";
        }

}