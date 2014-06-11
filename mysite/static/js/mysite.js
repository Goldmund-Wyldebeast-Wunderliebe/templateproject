/* Hightlight the current <li> in the navbar by adding a "active" class
 */

$('ul.navbar-nav li > a').each(function() {
    var current_path = window.location.pathname;
    var item_path = $(this).attr('href');
    if (current_path.indexOf(item_path)===0)
        $(this).parent().addClass('active');
});
