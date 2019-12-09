$(function () {
    var menuItem = $('#left-sidebar-menu-dashboard');
    menuItem.addClass('active');
    var subMenuItem = menuItem.find('#left-sidebar-menu-dashboard-MyVizzes');
    subMenuItem.addClass('active');

    $('.breadcrumb').hide();
});