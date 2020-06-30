def side_nav(request):
    nav_dict = {}
    content = ""
    if request.user.is_authenticated:
        nav_dict['Wiadomości'] = 'messages'
        if request.user.groups.filter(name='teachers'):
            nav_dict['Przedmioty'] = 'subjects'
            nav_dict['Oceny'] = 'grades'
        if request.user.groups.filter(name='students'):
            nav_dict['Oceny'] = 'student_grades'
        nav_dict['Logout'] = 'logout'
    return {'side_nav': nav_dict, 'content': content}
