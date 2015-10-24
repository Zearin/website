# Copyright Designbootstrap (theme light-wave)
# Copyright Gerard Krol
# License: MIT
import string
import markdown
import re
import settings

# Python 2 compatibility
def nop2(x,y):
    return x
try:
    unicode = unicode
except:
    unicode = nop2

# This function will pass unicode text right through, other text will be decoded as utf-8
def force_unicode(text):
    if repr(text)[0] == 'u': #FIXME...
        return text
    return unicode(text.strip(),"utf-8")

# Shorter way to encode markdown, also strips leading and trailing whitespace
def md(text):
    return markdown.markdown(force_unicode(text.strip()))
    
class Section(object):
    # slug, title, content
    direct_link = None # put a link in this variable to link directly to an external page
    def generate(self):
        return section(self.slug, self.title, self.get_content())

class Page(object):
    # slug, title
    hidden = False
    sections = []
    first_section_in_menu = False
    def generate(self, language, site_menu):
        section_content = "".join([force_unicode(x.generate()) for x in self.sections if not x.direct_link])
        return html(head("Freenet - " + self.title), body(
            force_unicode(menu(site_menu, self))+section_content))
    
def html(head, body):
    template = """
<!DOCTYPE html>
<html lang="en" class="no-js" >
$head
$body
</html>
"""
    return string.Template(template).substitute(head=head, body=body)

def head(title):
    template = """
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
<meta name="description" content="" />
<meta name="author" content="" />

<!-- Favicons start -->
<!-- generated by realfavicongenerator.net -->
<link rel="apple-touch-icon" sizes="57x57" href="assets/img/favicons/apple-touch-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="assets/img/favicons/apple-touch-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="assets/img/favicons/apple-touch-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="assets/img/favicons/apple-touch-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="assets/img/favicons/apple-touch-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="assets/img/favicons/apple-touch-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="assets/img/favicons/apple-touch-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="assets/img/favicons/apple-touch-icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/img/favicons/apple-touch-icon-180x180.png">
<link rel="icon" type="image/png" href="assets/img/favicons/favicon-32x32.png" sizes="32x32">
<link rel="icon" type="image/png" href="assets/img/favicons/favicon-194x194.png" sizes="194x194">
<link rel="icon" type="image/png" href="assets/img/favicons/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/png" href="assets/img/favicons/android-chrome-192x192.png" sizes="192x192">
<link rel="icon" type="image/png" href="assets/img/favicons/favicon-16x16.png" sizes="16x16">
<link rel="manifest" href="assets/img/favicons/manifest.json">
<link rel="shortcut icon" href="assets/img/favicons/favicon.ico">
<meta name="msapplication-TileColor" content="#2b5797">
<meta name="msapplication-TileImage" content="assets/img/favicons/mstile-144x144.png">
<meta name="msapplication-config" content="assets/img/favicons/browserconfig.xml">
<meta name="theme-color" content="#ffffff">
<!-- favicons end -->

<!--[if IE]>
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<![endif]-->
<title>$title</title>
<!-- BOOTSTRAP CORE CSS -->
<link href="assets/css/bootstrap.css" rel="stylesheet" />
<!-- ION ICONS STYLES -->
<link href="assets/css/ionicons.css" rel="stylesheet" />
<!-- FONT AWESOME ICONS STYLES -->
<link href="assets/css/font-awesome.css" rel="stylesheet" />
<!-- CUSTOM CSS -->
<link href="assets/css/style-freenet-3.css" rel="stylesheet" />
<!-- SLICK CAROUSEL -->
<!-- Kept in one directory instead of split to stay with upstream. -->
<link rel="stylesheet" type="text/css" href="assets/slick/slick.css"/>
<link rel="stylesheet" type="text/css" href="assets/slick/slick-theme.css"/>
<!-- HTML5 Shiv and Respond.js for IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
<!--[if lt IE 9]>
<script src="assets/js/html5shiv.js"></script>
<script src="assets/js/respond.min.js"></script>
<![endif]-->

</head>
"""
    return string.Template(template).substitute(title=title)
    
def body(content):
    template = """    
<body data-spy="scroll" data-target="#menu-section">

$content

<!-- JAVASCRIPT FILES PLACED AT THE BOTTOM TO REDUCE THE LOADING TIME -->
<!-- CORE JQUERY -->
<script src="assets/js/jquery-1.11.1.js"></script>
<!-- BOOTSTRAP SCRIPTS -->
<script src="assets/js/bootstrap.js"></script>
<!-- EASING SCROLL SCRIPTS PLUGIN -->
<script src="assets/js/jquery.easing.min.js"></script>
<!-- ISOTOPE SCRIPTS -->
<script src="assets/js/jquery.isotope.js"></script>
<!-- VIEWPORT ANIMATION SCRIPTS   -->
<script src="assets/js/appear.min.js"></script>
<!-- CUSTOM SCRIPTS -->
<script src="assets/js/custom.js"></script>
<!-- SLICK CAROUSEL -->
<script type="text/javascript" src="assets/slick/slick.min.js"></script>

</body>
"""
    return string.Template(template).substitute(content=content)

def menu(site_menu, current_page):
    menu_content = "";
    for page in site_menu:
        if page.hidden: continue
        filename = page.slug + ".html"
        if page.slug == current_page.slug:
            filename = ""
        section = ""
        if not page.first_section_in_menu:
            section = page.sections[0].slug
        menu_content += string.Template("""<li><a href="$filename#$section">$title</a></li>""").substitute(filename=filename,section=section,title=page.title.upper())
    submenu_content = ""
    if current_page.first_section_in_menu:
        skip = 0
    else:
        skip = 1
    for section in current_page.sections[skip:]:
        link = section.direct_link or "#" + section.slug
        submenu_content += string.Template("""<li><a href="$link">$title</a></li>""").substitute(link=link,title=section.title.upper())
    languages = ""
    for language in settings.languages:
        languages += string.Template(
            """<li><a href="?language=$language">$title</a></li>"""
        ).substitute(language=language, title=language.upper())
    template = """
<!--MENU SECTION START-->
<div class="navbar navbar-inverse navbar-fixed-top" id="menu-section" >
<div class="container">


<div class="navbar-header">
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
<span class="icon-bar"></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
</button>

<div class="navbar-brand">
    <a href="index.html">
        <img src="assets/img/logo_65_49.png" style="height: 2em;" alt="$rabbit"/>
        $brand
    </a>
</div>
</div>

<!-- languages -->
<div class="navbar-collapse collapse navbar-language">
<ul class="nav navbar-nav navbar-nav-language navbar-right">

$languages

</ul>
</div>


<div class="navbar-collapse collapse">
    <ul class="nav navbar-nav navbar-nav-page navbar-right">
        $menu_content
    </ul>
</div>

<div class="navbar-collapse collapse">
<ul class="nav navbar-nav navbar-right">

$submenu_content

</ul>
</div>

</div>
</div>
<!--MENU SECTION END-->
"""
    return string.Template(template).substitute(
        brand="FREENET", rabbit=_("Freenet rabbit logo"),
        menu_content=menu_content, submenu_content=submenu_content,
        languages=languages
    )

class ContactSection(Section):
    def __init__(self):
        self.slug = "contact"
        self.title = _("Contact")
    def get_content(self):
        template = """
<div class="row">

<div class="col-xs-12 col-sm-6 col-md-6 col-lg-6">
<div class="contact-wrapper">
<h3>Contact</h3>
<h4><strong>$press : </strong><span class="e-mail" data-user="sserp" data-website="gro.tcejorpteneerf"></span></h4>
<h4><strong>$support : </strong> support@freenetproject.org </h4>
<h4><strong>$irc : </strong> #freenet on chat.freenode.net</h4>
</div>

</div>
<div class="col-xs-12 col-sm-6 col-md-6 col-lg-6">
<div class="contact-wrapper">
<h3>$license_header</h3>
$license
<div class="footer-div" >
&copy; 2015 The Freenet Project Inc<br/>
<a href="http://www.designbootstrap.com/" target="_blank" >$design</a>
</div>
</div>

</div>
"""
        return string.Template(template).substitute(
            press=_("Press"),
            support=_("Support"),
            irc=_("IRC"),
            license_header=_("License"),
            license=_("Content on this website is licensed under the GNU Free Documentation License and may be available under other licenses."),
            design=_("Design by DesignBootstrap")
            )


def section(name, title, content):
    template = """
<!--section $name start-->
<section id="$name" >
<div class="container">
<div class="row text-center header">
<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">

<h3>$title</h3>
<hr />
</div>
</div>

$content

</section>
<!-- section $name end -->
"""
    return string.Template(template).substitute(name=name, title=title,content=content)

def text(content):
    template = """
<!-- text start -->
<div class="row">
<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
$content
</div>
</div>
<!-- text end -->
"""
    return string.Template(template).substitute(content=content)
