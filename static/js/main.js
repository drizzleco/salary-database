$('.has-clear input[type="text"]').on('input propertychange', function () {
    var $this = $(this);
    var visible = Boolean($this.val());
    $this.siblings('.form-control-clear').toggleClass('d-none', !visible);
}).trigger('propertychange');

$('.form-control-clear').click(function () {
    $(this).siblings('input[type="text"]').val('')
        .trigger('propertychange').focus();
});

function dateSorter(a, b) {
    if (new Date(a) < new Date(b)) return 1;
    if (new Date(a) > new Date(b)) return -1;
    return 0;
}

function linkFormatter(value, row, index, field) {
    if (field === 'EMPLOYER_NAME')
        return "<a href=\"?employer=" + value + "\">" + value + "</a>"
    if (field === 'JOB_TITLE')
        return "<a href=\"?title=" + value + "\">" + value + "</a>"
}

var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
});

function salaryFormatter(value) {
    return formatter.format(value);
}
