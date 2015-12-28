from django.template import Library, Node, TemplateSyntaxError, Variable
from accounts.models import BlockList
from django.template import Node

register = Library()

class RenderBlockList(Node):
    
    def __init__(self, user, var_name):
        self.user = Variable(user)
        self.var_name = var_name
        
    def render(self, context):
        user = self.user.resolve(context)
        try:
            block_list_qs = BlockList.objects.get(user=user.id)
            block_list = list(block_list_qs.blockedlist.all())
            context[self.var_name] = block_list
        except BlockList.DoesNotExist:
            context[self.var_name] = []
       
        return ''

@register.tag   
def block_list(parser,token):
    try:
        tag_name, user, word, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a four arguments" % token.contents.split()[0])
    print var_name
    return RenderBlockList(user,var_name)

