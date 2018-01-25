window.onload = function () {
    var edit_content = document.getElementById('update_content');
    var p_tag = document.getElementById('p_content')
    edit_content.onclick = function () {
        p_content = p_tag.innerHTML;
        document.removeChild(p_tag);
        0
        var input = document.createElement("input");
        input.setAttribute("value", "content")
        input.innerHTML = p_content;
    }

    //点击提问显示Message对话框

}
