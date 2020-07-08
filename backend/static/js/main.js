/**
 * Toggle clear button on search field appropriately on input
 */
$('.has-clear input[type="text"]').on('input propertychange', function () {
    var $this = $(this);
    var visible = Boolean($this.val());
    $this.siblings('.form-control-clear').toggleClass('d-none', !visible);
}).trigger('propertychange');

/**
 * Click handler for clear button on search fields that clears the field
 */
$('.form-control-clear').click(function () {
    $(this).siblings('input[type="text"]').val('')
        .trigger('propertychange').focus();
});

/**
 * Sort salaries table by the date column
 */
function dateSorter(a, b) {
    if (new Date(a) < new Date(b)) return 1;
    if (new Date(a) > new Date(b)) return -1;
    return 0;
}

/**
 * Format employer and job title column with value as a link
 */
function linkFormatter(value, row, index, field) {
    if (field === 'employer_name')
        return "<a href=\"?employer=" + value + "\">" + value + "</a>"
    if (field === 'job_title')
        return "<a href=\"?title=" + value + "\">" + value + "</a>"
    if (field === 'employer_city')
        return "<a href=\"?city=" + value + "\">" + value + "</a>"
    if (field === 'employer_state')
        return "<a href=\"?state=" + value + "\">" + value + "</a>"
}

var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
});

/**
 * Format Number as a USD currency string w/o decimals (123456.0 -> $123,456)
 */
function salaryFormatter(value) {
    return formatter.format(value);
}
