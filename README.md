RiggingDocker
==============

Ferramentas do team Rigging.


Notas
-----
* Caminho do repositorio: `C:\Users\userName\AppData\Roaming\VetorLobo\MayaAppDir\scripts`

Adicionar funcionalidades (MISC tab)
------------------------------------
Todas as mudanças necesarias são levadas a cabo no arquivo [vzRigWindow](PopoTools/vzRigWindow/__init__.py)
#### Adicionar um caminho dos icones: 
Ir à função `setIconsPath`:
```python
    @staticmethod
    def setIconsPath():
        os.environ['XBMLANGPATH'] += ';' + os.path.dirname( __file__ )
        os.environ['XBMLANGPATH'] += ';' + os.path.join(os.path.dirname( __file__ ), os.pardir, 'dslSculptInbetweenEditor')
        os.environ['XBMLANGPATH'] += ';' + os.path.join(os.path.dirname( __file__ ), os.pardir, 'shapeTools')
        os.environ['XBMLANGPATH'] += ';' + os.path.join(os.path.dirname( __file__ ), os.pardir, 'vzRM2')
```
#### Adicionar um caminho dos mel sripts: 
Ir à função `setIconsPath`:
```python
    @classmethod
    def setMelScriptsPath(cls):
        """ Adds custom functionality to Outliner's right-click menu """
        os.environ['MAYA_SCRIPT_PATH'] += ';' + os.path.dirname( __file__ )
        mel.eval('source outlinerEdMenuUserCallback') # Built-in script name that gets called on Maya's default Outliner initialization

        shapeToolsMel = os.path.join(os.path.dirname( __file__ ), os.pardir, 'shapeTools', 'mel')
        os.environ['XBMLANGPATH'] += ';' + shapeToolsMel
        files = [f for f in cls.getMelFiles(shapeToolsMel) if f != 'shapeToolsSetup.mel']
        for f in files: mel.eval('source ' + f)
```
#### Adicionar botão ao MISC tab
Ir à função `createMiscTab`:
```python
    def createMiscTab(self):
        ...
        # ADD MISC BUTTONS AREA

        # Function calls
        cearaSculptCall = lambda e: cearaSculpt.SculptInbetweenEditor().ui()
        mirrorShape = lambda e: mel.eval('performMirrorShape 1')
        copyShape = lambda e: mel.eval('evalEcho copyShape')
        mirrorSelection = lambda e: mel.eval('performMirrorSelection 1')
        copySelection = lambda e: mel.eval('evalEcho copySelection')
        vzRM2Call = lambda e: vzRM2.vzRM2.vzRM2()
```
Lambda é uma função que permite a creação de variaveis que representam uma função.
Assim: `cearaSculptCall = lambda e: cearaSculpt.SculptInbetweenEditor().ui()`
é equivalente a:
```python
def cearaSculptCall(e):
    cearaSculpt.SculptInbetweenEditor().ui()
```
A função que sera chamada quando o botão for clickado é enviada como variável no parámetro `command(c)`:
`cmds.symbolButton( image=img, ann=annotation, c=func, p=parent_id )`.
<br/>
A variável `func` deve representar uma função que receve um argumento, é por isso que as funções criadas com 
lambda recevem uma variavel `e` que representará o evento (mesmo quando elas não a usam).
<br/>
<br/>
Continuamos criando uma lista com os dados necessarios para a criação dos botões:
`(nome_da_imagem_do_botão, anotações, funcão_a_ser_executada_quando_o_botão_for_clickado)`
```python
        # Button's metadata structure: (icon, annotation, function call)
        btnsMetadata = [('im_zeroOut.png', 'ZeroOut selected object(s).', partial(self.zeroOut)),
                        ('im_zeroJoints.png', 'ZeroJoints selected object(s).', partial(self.zeroJoints, 0)),
                        ('im_setupLayers.png', 'Setup MESH and CTRL layers.', partial(self.setupLayers, 0)),
                        ('im_resetControls.png', 'Resets transforms and attributes of selected objects to 0. '\
                                + 'Or all "*ctrl" if nothing is selected.',
                                partial(self.doResetControls)),
                        ('dslSieIcon.xpm', 'Ceara Sculpt', cearaSculptCall),
                        ('mirrorShape.xpm', "Mirror Shape Options. Select source object or its components and symmetric object.",
                            mirrorShape),
                        ('copyShape.xpm', "Copy Shape. Select source object or its components and destination object(s).",
                            copyShape),
                        ('mirrorSelection.xpm', "Mirror Selection Options. Select vertices and symmetric object if the object is not symmetric.",
                            mirrorSelection),
                        ('copySelection.xpm', "Copy Selection. Select CV or vertices and the destination object(s).",
                            copySelection),
                        ('',"Run vzRM2", vzRM2Call)]
        # Add buttons to layout
        for img, annotation, func in btnsMetadata:
            cmds.symbolButton( image=img, ann=annotation, c=func, p=miscGl )
        ...
```

