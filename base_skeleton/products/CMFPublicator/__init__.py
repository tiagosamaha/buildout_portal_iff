##############################################################################
#
# Copyright (c) 2004 Dinheiro Vivo <www.dinheirovivo.com.br>
#                    by Jean Rodrigo Ferri <jeanrodrigoferri@yahoo.com.br>
# 
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
##############################################################################

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

import sys
import PublicatorTool

publicator_globals = globals()

registerDirectory('skins', publicator_globals)

tools = (PublicatorTool.PublicatorTool,)

this_module = sys.modules[__name__]

z_tool_bases = utils.initializeBasesPhase1(tools, this_module)

def initialize(context):

    utils.initializeBasesPhase2(z_tool_bases, context)

    context.registerHelpTitle('CMF Publicator Help')
    context.registerHelp(directory='help')

    utils.ToolInit ('CMF Publicator Tool',
                    tools=tools,
                    product_name='CMFPublicator',
                    icon='tool.gif'
                   ).initialize(context)

