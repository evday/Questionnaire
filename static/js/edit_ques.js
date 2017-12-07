/**
 * Created by haier on 2017-12-08.
 */

$(".question_list").on("click", ".fork", function () {
    $(this).parent().parent().remove()
});
$('.add_question').click(function () {
    s = '<li><div class="pk"><div class="form-group"><label for="id_caption" class="col-md-2 control-label">问题名称：</label><div class="col-md-10"><textarea name="caption" cols="60" rows="2" class="form-control" maxlength="64" required="" id="id_caption"></textarea></div></div><div class="form-group"><label for="id_ct" class="col-md-2 control-label">问题类型：</label><div class="col-md-3"><select name="ct" class="form-control" required="" id="id_ct"><option value="" selected="">---------</option> <option value="1">打分</option> <option value="2">单选</option><option value="3">评价</option></select><ul></ul></div><div class="col -md-2"><span style="font-size: 20px" class="add_choice"><a href="#add_choice" class="hide"> +添加选项</a></span></div></div><ul class="choice_list"></ul><span class="fork">×</span></div></li>';

    $(".form-horizontal").append(s)
});

var form_l = $("form.form-horizontal");
form_l.on("click", ".add_choice", function () {
    s = '<div> <div class="row col-md-10" style="margin-bottom: 10px"> <label for="id_name" class="col-md-2 control-label">●&nbsp;内容：</label> <div class="col-md-3"> <input type="text" name="name" value="" class="form-control" maxlength="32" required="" id="id_name"> </div> <label for="id_score" class="col-md-2 control-label">分值：</label> <div class="col-md-3"> <input type="text" name="score" value="" class="form-control" required="" id="id_score"> </div> </div> </div>';
    $(this).parent().parent().next().append(s)
});
form_l.on("change", "[name=ct]", function () {
    if ($(this).val() == 2) {
        $(this).parent().next().children().children().removeClass("hide")
    }
    else {
        $(this).parent().next().children().children().addClass("hide");
        $(this).parent().parent().next().children().remove()
    }

});
