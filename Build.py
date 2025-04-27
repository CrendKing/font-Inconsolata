import os
import subprocess

from glyphsLib import GSFont

if __name__ == '__main__':
    TRANSFORMATION = (1.05, 0, 0, 1.15, 0, 0)
    ADVANCE = 1.1
    OUTPUT_FILE = 'Inconsolata My.glyphs'

    font = GSFont('sources/Inconsolata.glyphs')

    font.versionMinor += 1

    width_axis_index = 0
    new_axes = []
    new_instances = []
    new_masters = []

    for i, axis in enumerate(font.axes):
        if axis.name == 'Width':
            width_axis_index = i
        else:
            new_axes.append(axis)

    for instance in font.instances:
        if 'Condensed' not in instance.name and 'Expanded' not in instance.name:
            if len(instance.axes) > width_axis_index:
                del instance.axes[width_axis_index]

            new_instances.append(instance)

    for master in font.masters:
        if 'Condensed' not in master.name and 'Expanded' not in master.name:
            if len(master.axes) > width_axis_index:
                del master.axes[width_axis_index]

            new_masters.append(master)

    font.axes = new_axes
    font.instances = new_instances
    font.masters = new_masters
    remaining_master_ids = {master.id for master in font.masters}

    for glyph in font.glyphs:
        glyph.layers = [layer for layer in glyph.layers if (layer.associatedMasterId or layer.layerId) in remaining_master_ids]

        for layer in glyph.layers:
            layer.width *= ADVANCE

            for path in layer.paths:
                path.applyTransform(TRANSFORMATION)

            for component in layer.components:
                component.applyTransformation(TRANSFORMATION[0], TRANSFORMATION[3])

            # remove corner component hints, which can't be processed by glyphsLib >= 6.2.0
            if any(h.type.upper() == 'CORNER' for h in layer.hints):
                layer.hints = []

    font.save(OUTPUT_FILE)

    subprocess.check_call(['gftools', 'builder', 'config.yaml'])
    os.remove('build.ninja')
    os.remove('.ninja_log')
    os.remove(OUTPUT_FILE)
