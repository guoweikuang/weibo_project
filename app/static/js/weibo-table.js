
$(function () {
    $('#screen').bootstrapTable({
        url: "/screen/list",
        dataFields: "rows",
        cache: false,
        striped: true,
        pagination: true,
        pageSize: 10,
        pageNumber: 1,
        pageList: [10, 20, 50],
        search: true,
        showRefresh: true,
        clickToselect: true,
        toolbar: "#toolbar_screen",
        sidePagination: "server",
        queryParamsType: "limit",

        columns: [{
            field: "id",
            title: "ID",
            align: "center",
            valign: "middle",
        }, {
            field: "content",
            title: "微博内容",
            align: "center",
            valign: "middle",
        }, {
            field: "pub_time",
            title: "发布时间",
            align: "center",
            valign: "middle",

        }, {
            field: "comment",
            title: "评论数",
            align: "center",
            valign: "middle",
        }, {
            field: "like",
            title: "点赞数",
            align: "center",
            valign: "middle",
        }],
        formatNoMatches: function () {
            return "无符合条件的记录";
        }
    });
    $(window).resize(function () {
        $('#screen').bootstrapTable('resetView');
    });
});


function infoFormatter(value, row, index) {
    return '<a href=/screen/' + row.id + ' target="_blank">' + row.name + '</a>';
}