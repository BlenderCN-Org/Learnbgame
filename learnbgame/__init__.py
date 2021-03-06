# <pep8 compliant>

# ----------------------------------------------------------
# Author: Fofight
# ----------------------------------------------------------


bl_info = {
    'name': 'Learnbgame',
    'description': 'Learn by game',
    'author': 'Fofight',
    'license': 'GPL',
    'version': (1, 0, 0),
    'blender': (2, 80, 0),
    'location': 'View3D > Tools > Learnbgame',
    'warning': '',
    'wiki_url': 'https://github.com/BlenderCN/Learnbgame/wiki',
    'tracker_url': 'https://github.com/BlenderCN/Learnbgame/issues',
    'link': 'https://github.com/BlenderCN/Learnbgame',
    'support': 'COMMUNITY',
    'category': 'Add Mesh'
    }
##########################Import Module############################

import os

import sys
sys.path.append(sys.path.append("/root/Software/anaconda3/lib/python3.7/site-packages"))
import openbabel
import pybel

import json

import bgl,blf

import bpy

from math import acos

from mathutils import Vector

from bpy.types import (
    Panel, 
    Operator,
    Menu,
    PropertyGroup,
    SpaceView3D,
    WindowManager,
    )

from bpy.props import (
    EnumProperty,
    PointerProperty,
    StringProperty,
    BoolProperty,
    )
from bpy.utils import (
    previews,
    register_class,
    unregister_class
    )

##########################Import Module############################

##########################Variable################################

icons_collection = {}
    
icons = previews.new()
icons_dir = os.path.join(os.path.dirname(__file__), "icons")
for icon in os.listdir(icons_dir):
    name, ext = os.path.splitext(icon)
    icons.load(name, os.path.join(icons_dir, icon), 'IMAGE')
icons_collection["main"] = icons

atoms_dir = os.path.join(os.path.dirname(__file__), "atoms")
atoms_file = open(os.path.join(atoms_dir,"atoms.json"))
atoms_list = json.load(atoms_file)

molecules_dir = os.path.join(os.path.dirname(__file__), "molecules")
with open(os.path.join(molecules_dir, 'atoms.json')) as in_file:
    atom_data = json.load(in_file)


animals_dir = os.path.join(os.path.dirname(__file__), "species/animal")
animals_list = os.listdir(animals_dir)

plants_dir = os.path.join(os.path.dirname(__file__), "species/plant")
plants_list = os.listdir(plants_dir)

micrabes_dir = os.path.join(os.path.dirname(__file__), "species/micrabe")
micrabes_list = os.listdir(micrabes_dir)

planets_dir = os.path.join(os.path.dirname(__file__), "planets")
planets_list = os.listdir(planets_dir)

icons_dir = os.path.join(os.path.dirname(__file__), "icons")
icons_list = os.listdir(icons_dir)

##########################Variable################################

########################UI##################################
class LEARNBGAME_ATOM(Panel):
    bl_idname = "learnbgame.atom"
    bl_label = "Atom"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Learnbgame"

    def draw(self,context):
        layout = self.layout
        scene = context.scene
        atoms = scene.atoms
        row = layout.row()
        row.prop(atoms,"atom",icon="PHYSICS")
        row.operator(ATOM_ADD.bl_idname,text="add",icon="ADD")

class LEARNBGAME_BRAND(Panel):
    bl_idname = "learnbgame.brand"
    bl_label = "Learnbgame"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Learnbgame"

    def draw(self,context):
        layout = self.layout
        scene = context.scene

        brand = scene.brand
        row = layout.row()
        row.prop(brand,"brand_text",icon="SMALL_CAPS")
        if context.window_manager.brand_run_opengl is False:
            icn = "PLAT",
            txt = "show"
        else:
            icon="PAUSE"
            txt = "hide"
        row.operator(BRAND_DISPLAY.bl_idname,text="show",icon="PLAY")


class LEARNBGAME_MOLECULE(Panel):
    bl_idname = "learnbgame.molecule"
    bl_label = "Molecule"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Learnbgame"

    global icons_collection
    icons = icons_collection["main"]

    def draw(self,context):
        layout = self.layout
        scene = context.scene

        molecule = scene.molecule
        row = layout.row()
        row.prop(
            molecule,
            "smile_format",
            icon_value=icons['molecule'].icon_id
            )
        row.operator(MOLECULE_ADD.bl_idname,text="add",icon="ADD")



class LEARNBGAME_SPECIES(Panel):
    bl_idname = "learnbgame.species"
    bl_label = "Species"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Learnbgame"

    global icons_collection
    icons = icons_collection["main"]

    def draw(self,context):
        layout = self.layout
        scene = context.scene

        animals = scene.animals
        row = layout.row(align=True)
        row.prop(
            animals,
            "animal",
            icon_value=icons[animals.animal if animals.animal+".png" in icons_list else "learnbgame"].icon_id
            )
        row.operator(ANIMAL_ADD.bl_idname,text="add",icon="ADD")

        plants = scene.plants
        row = layout.row()
        row.prop(
            plants,
            "plant",
            icon_value=icons[plants.plant if plants.plant+".png" in icons_list else "learnbgame"].icon_id
            )
        row.operator(PLANT_ADD.bl_idname,text="add",icon="ADD")

        micrabes = scene.micrabes
        row = layout.row()
        row.prop(
            micrabes,
            "micrabe",
            icon_value=icons[micrabes.micrabe if micrabes.micrabe+".png" in icons_list else "learnbgame"].icon_id)
        row.operator(MICRABE_ADD.bl_idname,text="add",icon="ADD")


class LEARNBGAME_PLANET(Panel):
    bl_idname = "learnbgame.planet"
    bl_label = "Planet"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Learnbgame"

    def draw(self,context):
        layout = self.layout
        scene = context.scene
        planets = scene.planets
        row = layout.row()
        row.prop(planets,"planet",icon="SHADING_WIRE")
        row.operator(PLANET_ADD.bl_idname,text="add",icon="ADD")

##########################UI#####################################

#########################Property###################################

class ATOM_PROPERTY(PropertyGroup):
    
    atom_items = [(atom['symbol'],atom['name'],"add " + atom['name']) for atom in atoms_list]
    atom_items.insert(0,("ptable","PeriodicTable","add Periodic Table of chemistry element"))
    atom : EnumProperty(
        name = "Atoms",
        items= atom_items
        )

class BRAND_PROPERTY(PropertyGroup):
    brand_text : StringProperty(
        name = "Text",
        description="brand text",
        default="Learnbgame"
        )
    WindowManager.brand_run_opengl = BoolProperty(default=False)


class MOLECULE_PROPERTY(PropertyGroup):
    smile_format : StringProperty(
        name = "Smile",
        description="smile format",
        default="CCO"
        )

class SPECIES_PROPERTY(PropertyGroup):


    animal : EnumProperty(
        name = "Animals",
        items=[
        (
            animal_name,
            animal_name.capitalize(),
            "add "+ animal_name,
            )for animal_name in animals_list
        ]
        )

    plant : EnumProperty(

        name = "Plants",
        items=[
        (
            plant_name,
            plant_name.capitalize(),
            "add "+ plant_name,
            )for plant_name in plants_list
        ]
        )

    micrabe : EnumProperty(
        name = "Micrabes",
        items =[
        (
            micrabe_name,
            micrabe_name.capitalize(),
            "add "+ micrabe_name,
            )for micrabe_name in micrabes_list
        ]
        )

class PLANET_PROPERTY(PropertyGroup):
    planet : EnumProperty(
        name = "Planet",
        items= [
        (
            planet_name,
            planet_name.capitalize(),
            "add "+ planet_name,
            )for planet_name in planets_list
        ]
        )
##########################Property####################################

######################Species Execute######################
class ANIMAL_ADD(Operator):
    bl_idname = "species.animal"
    bl_label = "Animal+"

    def execute(self,context):
        animals = context.scene.animals
        animal_name = animals.animal
        bpy.ops.import_scene.obj(filepath=animals_dir+"/"+animal_name+"/"+animal_name+".obj")
        obj = context.selected_objects
        context.view_layer.objects.active=obj[0]
        bpy.ops.object.join()
        obj = context.selected_objects
        obj[0].name = animal_name
        obj[0].location = context.scene.cursor_location
        return {'FINISHED'}

class PLANT_ADD(Operator):
    bl_idname = "species.plant"
    bl_label = "Plant+"

    def execute(self,context):

        plants = context.scene.plants
        plant_name = plants.plant
        bpy.ops.import_scene.obj(filepath=plants_dir+"/" + plant_name + "/" + plant_name +".obj")
        obj = bpy.context.selected_objects
        bpy.context.view_layer.objects.active=obj[0]
        bpy.ops.object.join()
        obj = bpy.context.selected_objects
        obj[0].name = plant_name
        obj[0].location = bpy.context.scene.cursor_location
        return {'FINISHED'}

class MICRABE_ADD(Operator):
    bl_idname = "species.micrabe"
    bl_label = "Micrabe+"

    def execute(self,context):

        micrabes = context.scene.micrabes
        micrabe_name = micrabes.micrabe
        bpy.ops.import_scene.obj(filepath=micrabes_dir+"/" + micrabe_name + "/" + micrabe_name +".obj")
        obj = bpy.context.selected_objects
        bpy.context.view_layer.objects.active=obj[0]
        bpy.ops.object.join()
        obj = bpy.context.selected_objects
        obj[0].name = micrabe_name
        obj[0].location = bpy.context.scene.cursor_location
        return {'FINISHED'}

#########################Species Execute#######################

#########################Planet Execute###################################
class PLANET_ADD(Operator):
    bl_idname = "planet.add"
    bl_label = "Planet+"

    def execute(self,context):

        planets = context.scene.planets
        planet_name = planets.planet
        bpy.ops.import_scene.obj(filepath=planets_dir+"/" + planet_name + "/" + planet_name +".obj")
        obj = bpy.context.selected_objects
        bpy.context.view_layer.objects.active=obj[0]
        bpy.ops.object.join()
        obj = bpy.context.selected_objects
        obj[0].name = planet_name
        obj[0].location = bpy.context.scene.cursor_location
        return {'FINISHED'}

###########################Planet Execute########################################        

###########################Molecule Execute####################################
class MOLECULE_ADD(Operator):
    bl_idname = "molecule.add"
    bl_label = "Molecule+"

    def execute(self,context):
        self.draw_molecule(context,center=(0, 0, 0), show_bonds=True, join=True)

        return {'FINISHED'}

    def draw_molecule(self,context,center=(0, 0, 0), show_bonds=True, join=True):

        smile_text = context.scene.molecule.smile_format
        molecule = pybel.readstring("smi", smile_text)
        molecule.make3D()

        shapes = []

        bpy.ops.mesh.primitive_uv_sphere_add()
        sphere = bpy.context.object

        # Initialize bond material if it's going to be used.
        if show_bonds:
            bpy.data.materials.new(name='bond')
            bpy.data.materials['bond'].diffuse_color = atom_data['bond']['color']
            bpy.data.materials['bond'].specular_intensity = 0.2
            bpy.ops.mesh.primitive_cylinder_add()
            cylinder = bpy.context.object
            cylinder.active_material = bpy.data.materials['bond']

        for atom in molecule.atoms:
            element = atom.type
            if element not in atom_data:
                element = 'undefined'

            if element not in bpy.data.materials:
                key = element
                bpy.data.materials.new(name=key)
                bpy.data.materials[key].diffuse_color = atom_data[key]['color']
                bpy.data.materials[key].specular_intensity = 0.2

            atom_sphere = sphere.copy()
            atom_sphere.data = sphere.data.copy()
            atom_sphere.location = [l + c for l, c in
                                    zip(atom.coords, center)]
            scale = 1 if show_bonds else 2.5
            atom_sphere.dimensions = [atom_data[element]['radius'] *scale * 2] * 3
            atom_sphere.active_material = bpy.data.materials[element]
            bpy.context.scene.collection.objects.link(atom_sphere)
            shapes.append(atom_sphere)

        for bond in (openbabel.OBMolBondIter(molecule.OBMol) if show_bonds else []):
            start = molecule.atoms[bond.GetBeginAtom().GetIndex()].coords
            end = molecule.atoms[bond.GetEndAtom().GetIndex()].coords
            diff = [c2 - c1 for c2, c1 in zip(start, end)]
            cent = [(c2 + c1) / 2 for c2, c1 in zip(start, end)]
            mag = sum([(c2 - c1) ** 2 for c1, c2 in zip(start, end)]) ** 0.5

            v_axis = Vector(diff).normalized()
            v_obj = Vector((0, 0, 1))
            v_rot = v_obj.cross(v_axis)

            # This check prevents gimbal lock (ie. weird behavior when v_axis is
            # close to (0, 0, 1))
            if v_rot.length > 0.01:
                v_rot = v_rot.normalized()
                axis_angle = [acos(v_obj.dot(v_axis))] + list(v_rot)
            else:
                v_rot = Vector((1, 0, 0))
                axis_angle = [0] * 4
            order = bond.GetBondOrder()
            if order not in range(1, 4):
                sys.stderr.write("Improper number of bonds! Defaulting to 1.\n")
                bond.GetBondOrder = 1

            if order == 1:
                trans = [[0] * 3]
            elif order == 2:
                trans = [[1.4 * atom_data['bond']['radius'] * x for x in v_rot],
                         [-1.4 * atom_data['bond']['radius'] * x for x in v_rot]]
            elif order == 3:
                trans = [[0] * 3,
                         [2.2 * atom_data['bond']['radius'] * x for x in v_rot],
                         [-2.2 * atom_data['bond']['radius'] * x for x in v_rot]]

            for i in range(order):
                bond_cylinder = cylinder.copy()
                bond_cylinder.data = cylinder.data.copy()
                bond_cylinder.dimensions = [atom_data['bond']['radius'] * scale *2] * 2 + [mag]
                bond_cylinder.location = [c + scale * v for c,v in zip(cent, trans[i])]
                bond_cylinder.rotation_mode = 'AXIS_ANGLE'
                bond_cylinder.rotation_axis_angle = axis_angle
                bpy.context.scene.collection.objects.link(bond_cylinder)
                shapes.append(bond_cylinder)

        sphere.select_set(True)
        if show_bonds:
            cylinder.select_set(True)
        bpy.ops.object.delete()

        for shape in shapes:
            shape.select_set(True)
        bpy.context.view_layer.objects.active = shapes[0]
        bpy.ops.object.shade_smooth()
        if join:
            bpy.ops.object.join()

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.context.scene.update()
        obj = bpy.context.selected_objects
        obj[0].name = smile_text
        obj[0].location = bpy.context.scene.cursor_location

        return {'FINISHED'}


#############################Molecule Execute################################

############################Atom Execute###################################

class ATOM_ADD(Operator):
    bl_idname = "atom.add"
    bl_label = "atom+"

    def execute(self,context):
        if context.scene.atoms.atom == "ptable":
            self.ptable(context)
        else:
            self.draw_proton_electron(context)

        return {'FINISHED'}

    def ptable(self,context):
        
        names = [ele['name'] for ele in atoms_list]
        alias = [ele['symbol'] for ele in atoms_list]

        keylist = bpy.data.objects.keys()

        num = 0


        for y in range(9,-11,-2):
            for x in range(-17,19,2):
                if y == 9 and x <= 15 and x >=-15:
                    pass
                elif (y == 7 and x >=-13 and x <= 5) or (y==5 and x >=-13 and x <= 5):
                    pass

                elif (y == -1 and x ==-13) or (y == -3 and x == -13):
                    pass

                elif y == -5 and x >= -17 and x <= 17:
                    pass

                elif (y == -7 and x >=-17 and x <=-13) or (y == -9 and x >=-17 and x <=-13) :
                    pass
                else:
                    bpy.ops.mesh.primitive_cube_add(
                        size=2,
                        view_align=False,
                        enter_editmode=False,
                        location=(x, y, 0))
                    bpy.context.object.name = names[num]            
                    bpy.data.materials.new(name=names[num])
                    bpy.data.materials[names[num]].diffuse_color = (0,0,0,1)
                    bpy.context.object.active_material = bpy.data.materials[names[num]]

                    bpy.ops.object.text_add(
                        view_align=False,
                        enter_editmode=True,
                        location=(x,y,1))
                    bpy.context.object.name = alias[num]

                    bpy.ops.font.delete(type='PREVIOUS_WORD') 
                    bpy.ops.font.text_insert(text=alias[num])
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
                    bpy.context.object.location = (x,y,1)
                    bpy.data.materials.new(name=alias[num])
                    bpy.data.materials[alias[num]].diffuse_color = (1,0,0,1)
                    bpy.context.object.active_material = bpy.data.materials[alias[num]]
                    bpy.ops.object.convert()
                    bpy.data.objects[names[num]].select_set(True)
                    bpy.context.view_layer.objects.active=bpy.data.objects[names[num]]
                    bpy.ops.object.join()


                    num += 1

    def draw_proton_electron(self,context):

        cursor_loc = bpy.context.scene.cursor_location

        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(cursor_loc[0],cursor_loc[1],cursor_loc[2]))

        obj = bpy.context.selected_objects

        obj[0].name = "proton"

        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(cursor_loc[0]+5,cursor_loc[1],cursor_loc[2]))

        obj = bpy.context.selected_objects

        obj[0].name = "electron"

        bpy.context.object.parent = bpy.data.objects["proton"]

        bpy.context.object.rotation_mode = 'XYZ'

        proton = bpy.data.objects['proton']

        proton.rotation_euler = (0,0,0)

        proton.keyframe_insert(data_path="rotation_euler",index=1,frame=bpy.context.scene.frame_start)

        proton.rotation_euler = (0,6.28319,0)

        end_frame = bpy.context.scene.frame_end = 50

        proton.keyframe_insert(data_path='rotation_euler', index=1,frame=end_frame + 1)

        proton.select_set(True)

        bpy.context.view_layer.objects.active = proton

        bpy.context.area.type = 'GRAPH_EDITOR'             

        bpy.ops.graph.interpolation_type(type='LINEAR')     

        bpy.context.area.type = 'VIEW_3D'



        bpy.ops.screen.animation_play()


############################Atom Execute###################################

############################Brand Execute###################################

class BRAND_DISPLAY(Operator):
    bl_idname = "brand.display"
    bl_label = "brand display"
    _handler = None

    def handle_add(self,context):
        if BRAND_DISPLAY._handler is None:
            BRAND_DISPLAY._handler = SpaceView3D.draw_handler_add(
                self.draw_callback,
                (context,),
                "WINDOW",
                "POST_PIXEL"
                )
            context.window_manager.brand_run_opengl = True

    def handle_remove(self,context):
        if BRAND_DISPLAY._handler is not None:
            SpaceView3D.draw_handler_remove(BRAND_DISPLAY._handler,"WINDOW")
        BRAND_DISPLAY._handler = None
        context.window_manager.brand_run_opengl = False
    def execute(self,context):
        if context.area.type == 'VIEW_3D':
            if context.window_manager.brand_run_opengl is False:
                self.handle_add(context)
            else:
                self.handle_remove(context)
            return {'FINISHED'}
        else:
            self.report({'WARNING'},
                 "View3D not found, cannot run operator")

        return {'CANCELLED'}

    def draw_callback(self, context):
        """Draw on the viewports"""
        # BLF drawing routine
        brand = context.scene.brand
        text = brand.brand_text
        font_id = 0
        blf.position(font_id, 25, 45, 0)
        blf.size(font_id, 50, 72)
        blf.draw(font_id, text)
        
############################Brand Execute###################################


CLASSES = (
    SPECIES_PROPERTY,
    PLANT_ADD,
    LEARNBGAME_SPECIES,
    LEARNBGAME_ATOM,
    LEARNBGAME_MOLECULE,
    LEARNBGAME_PLANET,
    MOLECULE_PROPERTY,
    PLANET_PROPERTY,
    ANIMAL_ADD,
    PLANET_ADD,
    MICRABE_ADD,
    MOLECULE_ADD,
    ATOM_PROPERTY,
    ATOM_ADD,
    BRAND_PROPERTY,
    BRAND_DISPLAY,
    LEARNBGAME_BRAND,
    )

def register():

    for cla in CLASSES:
        register_class(cla)
    bpy.types.Scene.plants = PointerProperty(type=SPECIES_PROPERTY)
    bpy.types.Scene.animals = PointerProperty(type=SPECIES_PROPERTY)
    bpy.types.Scene.micrabes = PointerProperty(type=SPECIES_PROPERTY)
    bpy.types.Scene.planets = PointerProperty(type=PLANET_PROPERTY)
    bpy.types.Scene.molecule = PointerProperty(type=MOLECULE_PROPERTY)
    bpy.types.Scene.atoms = PointerProperty(type=ATOM_PROPERTY)
    bpy.types.Scene.brand = PointerProperty(type=BRAND_PROPERTY)



def unregister():
    global icons_collection
    for cla in CLASSES:
        unregister_class(cla)
    for icons in icons_collection.values():
        previews.remove(icons)
    icons_collection.clear()


if __name__ == "__main__":
    register()
