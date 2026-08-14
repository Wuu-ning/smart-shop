"""Update route references from / to /home"""
import os, glob

FRONTEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'src')

files = [
    'components/Navbar.vue',
    'views/Login.vue',
    'views/Cart.vue',
    'views/Orders.vue',
    'views/Favorites.vue',
]

for rel in files:
    path = os.path.join(FRONTEND, rel)
    if not os.path.exists(path):
        continue
    c = open(path, encoding='utf-8').read()
    old = c
    
    # Replace router.push('/') with router.push('/home')
    c = c.replace("$router.push('/')", "$router.push('/home')")
    c = c.replace("router.push('/')", "router.push('/home')")
    
    # But not if it's already /home
    # Fix $router.push("/") style
    c = c.replace('$router.push("/")', "$router.push('/home')")
    
    if c != old:
        open(path, 'w', encoding='utf-8').write(c)
        print(f'  Updated: {rel}')
    else:
        print(f'  No change: {rel}')

print('Done')
