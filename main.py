import math
from os import link
import re
from xml.etree import ElementTree
import random
import sys
import uuid
from xml.dom import minidom


nodeTypes = ["real", 'angle', 'vector', 'color']


def new_guid():
    return uuid.uuid4().hex


def getDefs(root):
    for item in root:
        if item.tag == "defs":
            exportedDefs = item
    try:
        exportedDefs
    except NameError:
        exportedDefs = ElementTree.Element('defs')
        root.insert(0, exportedDefs)

    return exportedDefs


def createReal(value, id=None):
    real = ElementTree.Element('real')
    real.set('value', str(value))

    if (id is not None):
        real.set('id', id)

    return real


def createAngle(value):
    angle = ElementTree.Element('angle')
    angle.set('value', str(value))

    return angle


def createVector(xValue, yValue):
    vector = ElementTree.Element('vector')

    x = ElementTree.SubElement(vector, 'x')
    x.text = str(xValue)

    y = ElementTree.SubElement(vector, 'y')
    y.text = str(yValue)

    return vector


def createColor(red, green, blue, alpha):
    color = ElementTree.Element('color')

    r = ElementTree.SubElement(color, 'r')
    r.text = str(red)

    g = ElementTree.SubElement(color, 'g')
    g.text = str(green)

    b = ElementTree.SubElement(color, 'b')
    b.text = str(blue)

    a = ElementTree.SubElement(color, 'a')
    a.text = str(alpha)

    return color


def createVectorX(toLink=None, linkExported=None, type='real'):
    vectorX = ElementTree.Element('vectorx')
    vectorX.set('type', type)
    if linkExported is not None:
        vectorX.set('vector', linkExported)

    if linkExported is None:
        vector = ElementTree.SubElement(vectorX, 'vector')
        vector.append(toLink)

    return vectorX


def createVectorY(toLink=None, linkExported=None, type='real'):
    vectorY = ElementTree.Element('vectory')
    vectorY.set('type', type)
    if linkExported is not None:
        vectorY.set('vector', linkExported)

    if linkExported is None:
        vector = ElementTree.SubElement(vectorY, 'vector')
        vector.append(toLink)

    return vectorY


def createReciprocal(toLink, linkExported=None, type='real'):
    reciprocal = ElementTree.Element('reciprocal')
    reciprocal.set('type', type)
    if linkExported is not None:
        reciprocal.set('link', linkExported)

    if linkExported is None:
        link = ElementTree.SubElement(reciprocal, 'link')
        link.append(toLink)

    epsilon = ElementTree.SubElement(reciprocal, 'epsilon')
    epsilon.append(createReal("0.0000010000"))

    infinite = ElementTree.SubElement(reciprocal, 'infinite')
    infinite.append(createReal(999999.0000000000))

    return reciprocal


def createScale(type="real", scalarLink=None, linkExported=None, toLink=None, scalarLinkExported=None):
    scale = ElementTree.Element('scale')
    scale.set('type', str(type))
    if linkExported is not None:
        scale.set('link', linkExported)

    if linkExported is None:
        link = ElementTree.SubElement(scale, 'link')
        link.append(toLink)

    if scalarLink is not None:
        scalar = ElementTree.SubElement(scale, 'scalar')
        scalar.append(scalarLink)
    else:
        scale.set("scalar", scalarLinkExported)

    return scale


def createSubtract(lhsLink, rhsLink, scalarLink, type):
    subtract = ElementTree.Element('subtract')
    subtract.set('type', type)

    scalar = ElementTree.SubElement(subtract, 'scalar')
    scalar.append(scalarLink)

    lhs = ElementTree.SubElement(subtract, 'lhs')
    lhs.append(lhsLink)

    rhs = ElementTree.SubElement(subtract, 'rhs')
    rhs.append(rhsLink)

    return subtract


def createAdd(lhsLink, rhsLink, scalarLink, type):
    add = ElementTree.Element('add')
    add.set('type', type)

    lhs = ElementTree.SubElement(add, 'lhs')
    lhs.append(lhsLink)

    rhs = ElementTree.SubElement(add, 'rhs')
    rhs.append(rhsLink)

    scalar = ElementTree.SubElement(add, 'scalar')
    scalar.append(scalarLink)

    return add


def createRange(minLink, maxLink, toLink, type, linkExported=None):
    range = ElementTree.Element('range')
    range.set('type', type)
    if linkExported is not None:
        range.set('link', linkExported)

    min = ElementTree.SubElement(range, 'min')
    min.append(minLink)

    max = ElementTree.SubElement(range, 'max')
    max.append(maxLink)

    if linkExported is None:
        link = ElementTree.SubElement(range, 'link')
        link.append(toLink)

    return range


def createPower(type, baseLink, powerRLink):
    power = ElementTree.Element('power')
    power.set('type', type)

    base = ElementTree.SubElement(power, 'base')
    base.append(baseLink)

    powerR = ElementTree.SubElement(power, 'power')
    powerR.append(powerRLink)

    epsilon = ElementTree.SubElement(power, 'epsilon')
    epsilon.append(createReal("0.0000010000"))

    infinite = ElementTree.SubElement(power, 'infinite')
    infinite.append(createReal("999999.0000000000"))
    return power


def createNode(value, nodeType=None):
    if nodeType == "real":
        return createReal(value)
    elif nodeType == "angle":
        return createAngle(value)
    elif nodeType == "vector":
        return createVector(*value)
    elif nodeType == "color":
        return createColor(*value)


def drawSliderUI(root, sliderName):
    sliderUI = ElementTree.fromstring(f'''
              <layer type="group" active="true" exclude_from_rendering="false" version="0.3" desc="{sliderName}">
                <param name="z_depth">
                <real value="0.0000000000"/>
                </param>
                <param name="amount">
                <real value="1.0000000000"/>
                </param>
                <param name="blend_method">
                <integer value="0" static="true"/>
                </param>
                <param name="origin">
                <vector>
                    <x>0.0000000000</x>
                    <y>0.0000000000</y>
                </vector>
                </param>
                <param name="transformation">
                <composite type="transformation">
                    <offset>
                    <vector>
                        <x>0.0000000000</x>
                        <y>0.0000000000</y>
                    </vector>
                    </offset>
                    <angle>
                    <angle value="0.000000"/>
                    </angle>
                    <skew_angle>
                    <angle value="0.000000"/>
                    </skew_angle>
                    <scale>
                    <vector>
                        <x>1.0000000000</x>
                        <y>1.0000000000</y>
                    </vector>
                    </scale>
                </composite>
                </param>
                <param name="canvas">
                <canvas>
                    <layer type="group" active="true" exclude_from_rendering="false" version="0.3" desc="Pointer">
                    <param name="z_depth">
                        <real value="0.0000000000"/>
                    </param>
                    <param name="amount">
                        <real value="1.0000000000"/>
                    </param>
                    <param name="blend_method">
                        <integer value="0" static="true"/>
                    </param>
                    <param name="origin">
                        <vector>
                        <x>0.0000000000</x>
                        <y>0.0000000000</y>
                        </vector>
                    </param>
                    <param name="transformation">
                        <composite type="transformation">
                        <offset>
                            <blinecalcvertex type="vector" amount=":{sliderName}">
                            <bline>
                                <bline type="bline_point">
                                <entry>
                                    <composite guid="737B1DBB99C7B6E8B0D40E94E1B20814" type="bline_point">
                                    <point>
                                        <vector>
                                        <x>-1.6666667461</x>
                                        <y>0.3333333433</y>
                                        </vector>
                                    </point>
                                    <width>
                                        <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                        <real value="0.9143519402"/>
                                    </origin>
                                    <split>
                                        <bool value="false"/>
                                    </split>
                                    <t1>
                                        <radial_composite type="vector">
                                        <radius>
                                            <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                            <angle value="-0.000000"/>
                                        </theta>
                                        </radial_composite>
                                    </t1>
                                    <t2>
                                        <radial_composite type="vector">
                                        <radius>
                                            <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                            <angle value="-0.000000"/>
                                        </theta>
                                        </radial_composite>
                                    </t2>
                                    <split_radius>
                                        <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                        <bool value="false"/>
                                    </split_angle>
                                    </composite>
                                </entry>
                                <entry>
                                    <composite guid="611C8C4EB7DCDFD0BC1BD4180A27F506" type="bline_point">
                                    <point>
                                        <vector>
                                        <x>1.6666667461</x>
                                        <y>0.3333333433</y>
                                        </vector>
                                    </point>
                                    <width>
                                        <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                        <real value="0.5000000000"/>
                                    </origin>
                                    <split>
                                        <bool value="false"/>
                                    </split>
                                    <t1>
                                        <radial_composite type="vector">
                                        <radius>
                                            <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                            <angle value="0.000000"/>
                                        </theta>
                                        </radial_composite>
                                    </t1>
                                    <t2>
                                        <radial_composite type="vector">
                                        <radius>
                                            <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                            <angle value="0.000000"/>
                                        </theta>
                                        </radial_composite>
                                    </t2>
                                    <split_radius>
                                        <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                        <bool value="false"/>
                                    </split_angle>
                                    </composite>
                                </entry>
                                </bline>
                            </bline>
                            <loop>
                                <bool value="false"/>
                            </loop>
                            <homogeneous>
                                <bool value="false"/>
                            </homogeneous>
                            </blinecalcvertex>
                        </offset>
                        <angle>
                            <angle value="0.000000"/>
                        </angle>
                        <skew_angle>
                            <angle value="0.000000"/>
                        </skew_angle>
                        <scale>
                            <vector>
                            <x>0.7100870013</x>
                            <y>0.7100870013</y>
                            </vector>
                        </scale>
                        </composite>
                    </param>
                    <param name="canvas">
                        <canvas>
                        <layer type="region" active="true" exclude_from_rendering="false" version="0.1" desc="Pointer">
                            <param name="z_depth">
                            <real value="0.0000000000"/>
                            </param>
                            <param name="amount">
                            <real value="1.0000000000"/>
                            </param>
                            <param name="blend_method">
                            <integer value="0"/>
                            </param>
                            <param name="color">
                            <color>
                                <r>1.000000</r>
                                <g>1.000000</g>
                                <b>1.000000</b>
                                <a>1.000000</a>
                            </color>
                            </param>
                            <param name="origin">
                            <vector>
                                <x>0.0000000000</x>
                                <y>0.0000000000</y>
                            </vector>
                            </param>
                            <param name="invert">
                            <bool value="false"/>
                            </param>
                            <param name="antialias">
                            <bool value="true"/>
                            </param>
                            <param name="feather">
                            <real value="0.0000000000"/>
                            </param>
                            <param name="blurtype">
                            <integer value="1"/>
                            </param>
                            <param name="winding_style">
                            <integer value="0"/>
                            </param>
                            <param name="bline">
                            <bline type="bline_point" loop="true">
                                <entry>
                                <composite guid="1E7B60652ED438133579BEBCE4DA83DF" type="bline_point">
                                    <point>
                                    <vector>
                                        <x>-0.4971296787</x>
                                        <y>0.4305267334</y>
                                    </vector>
                                    </point>
                                    <width>
                                    <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                    <real value="0.5000000000"/>
                                    </origin>
                                    <split>
                                    <bool value="false"/>
                                    </split>
                                    <t1>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t1>
                                    <t2>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t2>
                                    <split_radius>
                                    <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                    <bool value="false"/>
                                    </split_angle>
                                </composite>
                                </entry>
                                <entry>
                                <composite guid="F834BD4289D00B12E233D07DD05D32E5" type="bline_point">
                                    <point>
                                    <vector>
                                        <x>-0.2485648245</x>
                                        <y>-0.0000001187</y>
                                    </vector>
                                    </point>
                                    <width>
                                    <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                    <real value="0.5000000000"/>
                                    </origin>
                                    <split>
                                    <bool value="false"/>
                                    </split>
                                    <t1>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t1>
                                    <t2>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t2>
                                    <split_radius>
                                    <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                    <bool value="false"/>
                                    </split_angle>
                                </composite>
                                </entry>
                                <entry>
                                <composite guid="BEB92C43C03983CC4A7DF36D8FFE109A" type="bline_point">
                                    <point>
                                    <vector>
                                        <x>0.0000001685</x>
                                        <y>-0.4305270314</y>
                                    </vector>
                                    </point>
                                    <width>
                                    <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                    <real value="0.5000000000"/>
                                    </origin>
                                    <split>
                                    <bool value="false"/>
                                    </split>
                                    <t1>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="-0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t1>
                                    <t2>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="-0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t2>
                                    <split_radius>
                                    <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                    <bool value="false"/>
                                    </split_angle>
                                </composite>
                                </entry>
                                <entry>
                                <composite guid="1AD522C77A896F4382230F7154F7FECB" type="bline_point">
                                    <point>
                                    <vector>
                                        <x>0.2485648692</x>
                                        <y>-0.0000000890</y>
                                    </vector>
                                    </point>
                                    <width>
                                    <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                    <real value="0.5000000000"/>
                                    </origin>
                                    <split>
                                    <bool value="false"/>
                                    </split>
                                    <t1>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t1>
                                    <t2>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t2>
                                    <split_radius>
                                    <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                    <bool value="false"/>
                                    </split_angle>
                                </composite>
                                </entry>
                                <entry>
                                <composite guid="E492C2547BE39C4AA1E1A2DB3C2D40F9" type="bline_point">
                                    <point>
                                    <vector>
                                        <x>0.4971296489</x>
                                        <y>0.4305270314</y>
                                    </vector>
                                    </point>
                                    <width>
                                    <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                    <real value="0.5000000000"/>
                                    </origin>
                                    <split>
                                    <bool value="false"/>
                                    </split>
                                    <t1>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t1>
                                    <t2>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t2>
                                    <split_radius>
                                    <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                    <bool value="false"/>
                                    </split_angle>
                                </composite>
                                </entry>
                                <entry>
                                <composite guid="1CB8D031A10AF4D52A8A1B2999AB3DAE" type="bline_point">
                                    <point>
                                    <vector>
                                        <x>0.0000000102</x>
                                        <y>0.4305268228</y>
                                    </vector>
                                    </point>
                                    <width>
                                    <real value="1.0000000000"/>
                                    </width>
                                    <origin>
                                    <real value="0.5000000000"/>
                                    </origin>
                                    <split>
                                    <bool value="false"/>
                                    </split>
                                    <t1>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t1>
                                    <t2>
                                    <radial_composite type="vector">
                                        <radius>
                                        <real value="0.0000000000"/>
                                        </radius>
                                        <theta>
                                        <angle value="0.000000"/>
                                        </theta>
                                    </radial_composite>
                                    </t2>
                                    <split_radius>
                                    <bool value="true"/>
                                    </split_radius>
                                    <split_angle>
                                    <bool value="false"/>
                                    </split_angle>
                                </composite>
                                </entry>
                            </bline>
                            </param>
                        </layer>
                        </canvas>
                    </param>
                    <param name="time_dilation">
                        <real value="1.0000000000"/>
                    </param>
                    <param name="time_offset">
                        <time value="0s"/>
                    </param>
                    <param name="children_lock">
                        <bool value="true"/>
                    </param>
                    <param name="outline_grow">
                        <real value="0.0000000000"/>
                    </param>
                    <param name="z_range">
                        <bool value="false" static="true"/>
                    </param>
                    <param name="z_range_position">
                        <real value="0.0000000000"/>
                    </param>
                    <param name="z_range_depth">
                        <real value="0.0000000000"/>
                    </param>
                    <param name="z_range_blur">
                        <real value="0.0000000000"/>
                    </param>
                    </layer>
                    <layer type="advanced_outline" active="true" exclude_from_rendering="false" version="0.3" desc="Limits">
                    <param name="z_depth">
                        <real value="0.0000000000"/>
                    </param>
                    <param name="amount">
                        <real value="1.0000000000"/>
                    </param>
                    <param name="blend_method">
                        <integer value="0"/>
                    </param>
                    <param name="color">
                        <color>
                        <r>0.000000</r>
                        <g>0.000000</g>
                        <b>0.000000</b>
                        <a>1.000000</a>
                        </color>
                    </param>
                    <param name="origin">
                        <vector>
                        <x>0.0000000000</x>
                        <y>0.1666666716</y>
                        </vector>
                    </param>
                    <param name="invert">
                        <bool value="false"/>
                    </param>
                    <param name="antialias">
                        <bool value="true"/>
                    </param>
                    <param name="feather">
                        <real value="0.0000000000"/>
                    </param>
                    <param name="blurtype">
                        <integer value="1"/>
                    </param>
                    <param name="winding_style">
                        <integer value="0"/>
                    </param>
                    <param name="bline">
                        <bline guid="C19377D913E5ECE93151ED9E27B58259" type="bline_point">
                        <entry>
                            <composite guid="4BD115A9C2E2CA2D73C510FDD5B029E7" type="bline_point">
                            <point>
                                <vector>
                                <x>-1.6666667461</x>
                                <y>0.0833333358</y>
                                </vector>
                            </point>
                            <width>
                                <real value="1.0000000000"/>
                            </width>
                            <origin>
                                <real value="0.5000000000"/>
                            </origin>
                            <split>
                                <bool value="false"/>
                            </split>
                            <t1>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="0.000000"/>
                                </theta>
                                </radial_composite>
                            </t1>
                            <t2>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="180.000000"/>
                                </theta>
                                </radial_composite>
                            </t2>
                            <split_radius>
                                <bool value="true"/>
                            </split_radius>
                            <split_angle>
                                <bool value="false"/>
                            </split_angle>
                            </composite>
                        </entry>
                        <entry>
                            <composite guid="11FEE7C15F29985125A914EB159B9D49" type="bline_point">
                            <point>
                                <vector>
                                <x>-1.6666666269</x>
                                <y>-0.1666666716</y>
                                </vector>
                            </point>
                            <width>
                                <real value="1.0000000000"/>
                            </width>
                            <origin>
                                <real value="0.0735090971"/>
                            </origin>
                            <split>
                                <bool value="false"/>
                            </split>
                            <t1>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="-0.000000"/>
                                </theta>
                                </radial_composite>
                            </t1>
                            <t2>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="-0.000000"/>
                                </theta>
                                </radial_composite>
                            </t2>
                            <split_radius>
                                <bool value="true"/>
                            </split_radius>
                            <split_angle>
                                <bool value="false"/>
                            </split_angle>
                            </composite>
                        </entry>
                        <entry>
                            <composite guid="FA2CB23F728416598284FFF9058C403F" type="bline_point">
                            <point>
                                <vector>
                                <x>1.6666666269</x>
                                <y>-0.1666666716</y>
                                </vector>
                            </point>
                            <width>
                                <real value="1.0000000000"/>
                            </width>
                            <origin>
                                <real value="0.9143519402"/>
                            </origin>
                            <split>
                                <bool value="false"/>
                            </split>
                            <t1>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="-0.000000"/>
                                </theta>
                                </radial_composite>
                            </t1>
                            <t2>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="-0.000000"/>
                                </theta>
                                </radial_composite>
                            </t2>
                            <split_radius>
                                <bool value="true"/>
                            </split_radius>
                            <split_angle>
                                <bool value="false"/>
                            </split_angle>
                            </composite>
                        </entry>
                        <entry>
                            <composite guid="0F5A0FE11CC375D5273BF91F5BA8D5BC" type="bline_point">
                            <point>
                                <vector>
                                <x>1.6666667461</x>
                                <y>0.0833333358</y>
                                </vector>
                            </point>
                            <width>
                                <real value="1.0000000000"/>
                            </width>
                            <origin>
                                <real value="0.5000000000"/>
                            </origin>
                            <split>
                                <bool value="false"/>
                            </split>
                            <t1>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="0.000000"/>
                                </theta>
                                </radial_composite>
                            </t1>
                            <t2>
                                <radial_composite type="vector">
                                <radius>
                                    <real value="0.0000000000"/>
                                </radius>
                                <theta>
                                    <angle value="0.000000"/>
                                </theta>
                                </radial_composite>
                            </t2>
                            <split_radius>
                                <bool value="true"/>
                            </split_radius>
                            <split_angle>
                                <bool value="false"/>
                            </split_angle>
                            </composite>
                        </entry>
                        </bline>
                    </param>
                    <param name="width">
                        <real value="0.1666666719"/>
                    </param>
                    <param name="expand">
                        <real value="0.0000000000"/>
                    </param>
                    <param name="start_tip">
                        <integer value="1"/>
                    </param>
                    <param name="end_tip">
                        <integer value="1"/>
                    </param>
                    <param name="cusp_type">
                        <integer value="1"/>
                    </param>
                    <param name="smoothness">
                        <real value="1.0000000000"/>
                    </param>
                    <param name="homogeneous">
                        <bool value="true" static="true"/>
                    </param>
                    <param name="wplist">
                        <wplist type="width_point">
                        <entry>
                            <composite guid="930E9A57618A34B52050FD075CB4A4FA" type="width_point">
                            <position>
                                <real value="0.1000000000"/>
                            </position>
                            <width>
                                <real value="1.0000000000"/>
                            </width>
                            <side_before>
                                <integer value="0"/>
                            </side_before>
                            <side_after>
                                <integer value="0"/>
                            </side_after>
                            <lower_bound>
                                <real value="0.0000000000" static="true"/>
                            </lower_bound>
                            <upper_bound>
                                <real value="1.0000000000" static="true"/>
                            </upper_bound>
                            </composite>
                        </entry>
                        <entry>
                            <composite guid="F19F5B6B3033C1666EEBFAC91276FB6A" type="width_point">
                            <position>
                                <real value="0.9000000000"/>
                            </position>
                            <width>
                                <real value="1.0000000000"/>
                            </width>
                            <side_before>
                                <integer value="0"/>
                            </side_before>
                            <side_after>
                                <integer value="0"/>
                            </side_after>
                            <lower_bound>
                                <real value="0.0000000000" static="true"/>
                            </lower_bound>
                            <upper_bound>
                                <real value="1.0000000000" static="true"/>
                            </upper_bound>
                            </composite>
                        </entry>
                        </wplist>
                    </param>
                    <param name="dash_enabled">
                        <bool value="false"/>
                    </param>
                    <param name="dilist">
                        <dilist type="dash_item">
                        <entry>
                            <composite guid="2186D8210E86B568C60AFAD4B30DF6F9" type="dash_item">
                            <offset>
                                <real value="0.1000000000"/>
                            </offset>
                            <length>
                                <real value="0.1000000000"/>
                            </length>
                            <side_before>
                                <integer value="4"/>
                            </side_before>
                            <side_after>
                                <integer value="4"/>
                            </side_after>
                            </composite>
                        </entry>
                        </dilist>
                    </param>
                    <param name="dash_offset">
                        <real value="0.0000000000"/>
                    </param>
                    </layer>
                </canvas>
                </param>
                <param name="time_dilation">
                <real value="1.0000000000"/>
                </param>
                <param name="time_offset">
                <time value="0s"/>
                </param>
                <param name="children_lock">
                <bool value="false"/>
                </param>
                <param name="outline_grow">
                <real value="0.0000000000"/>
                </param>
                <param name="z_range">
                <bool value="false" static="true"/>
                </param>
                <param name="z_range_position">
                <real value="0.0000000000"/>
                </param>
                <param name="z_range_depth">
                <real value="0.0000000000"/>
                </param>
                <param name="z_range_blur">
                <real value="0.0000000000"/>
                </param>
            </layer>
        ''')
    root.append(sliderUI)


def createAdditions(valuesToAdd,  controllerIds, nodeType):
    for i in range(1, len(valuesToAdd)):
        if nodeType == 'real' or nodeType == "angle": 
            valuesToAdd[i] = valuesToAdd[i] - valuesToAdd[0]
        if nodeType == "vector":
                valuesToAdd[i] = [valuesToAdd[i][0] - valuesToAdd[0][0], valuesToAdd[i][1] - valuesToAdd[0][1]]
        if nodeType == "color":
                valuesToAdd[i] = [valuesToAdd[i][j] - valuesToAdd[0][j] for j in range(4)]
    addConvertedList = []
    if nodeType == "real" or nodeType == "angle":
        baseValue = createNode(valuesToAdd[0], nodeType)
    elif nodeType == "vector":
        baseValue = createNode(
            (valuesToAdd[0][0], valuesToAdd[0][1]), nodeType)
    elif nodeType == "color":
            baseValue = createNode(
                (valuesToAdd[0][0], valuesToAdd[0][1], valuesToAdd[0][2], valuesToAdd[0][3]), nodeType)
    addConvertedList.append(baseValue)
    for i in range(1, len(valuesToAdd)):
        if nodeType == "real" or nodeType == "angle":
                baseValue = createNode(valuesToAdd[i], nodeType)
        elif nodeType == "vector":
                baseValue = createNode(
                    (valuesToAdd[i][0], valuesToAdd[i][1]), nodeType)
        elif nodeType == "color":
                baseValue = createNode(
                    (valuesToAdd[i][0], valuesToAdd[i][1], valuesToAdd[i][2], valuesToAdd[i][3]), nodeType)
        toLinkValue = createNode(valuesToAdd[i], nodeType)
        addConvertedList.append(createScale(
            type=nodeType, toLink=toLinkValue, scalarLinkExported=controllerIds[i-1]))
    while (len(addConvertedList) >= 2):
        for i in range(math.ceil(len(addConvertedList)/2)):
            try:
                addConvertedList[i] = createAdd(
                    lhsLink=addConvertedList[i*2], rhsLink=addConvertedList[(i*2)+1], scalarLink=createReal("1.0"), type=nodeType)
            except:
                addConvertedList[i] = addConvertedList[i*2]
        for i in range(len(addConvertedList) - math.ceil(len(addConvertedList)/2)):
            del addConvertedList[-1]
    return addConvertedList[0]


def connectSlider(parentsToConnect, controllerIdsList, nodeType, fps, keyframes ):
        for parent in parentsToConnect:
            animated = parent[0]
            valuesToPass = []
            for waypoint in animated:
                for keyframe in keyframes:
                    waypointAtFrame = int(
                        round(float(waypoint.attrib['time'].replace("s", ""))*fps))
                    if (waypointAtFrame == keyframe):
                        if nodeType == "real" or nodeType == "angle":
                                valuesToPass.append(
                                    float(list(waypoint)[0].attrib['value']))
                        if nodeType == "vector":
                                valuesToPass.append([float(list(list(waypoint)[0])[0].text), float(
                                    list(list(waypoint)[0])[1].text)])
                        if nodeType == "color":
                                valuesToPass.append([float(list(list(waypoint)[0])[0].text), float(list(list(waypoint)[0])[
                                                    1].text), float(list(list(waypoint)[0])[2].text), float(list(list(waypoint)[0])[3].text)])
            for i in parent:
                parent.remove(i)
            parent.append(createAdditions(valuesToPass, controllerIdsList, nodeType))


root = ElementTree.parse(sys.argv[1]).getroot()

keyframes = root.findall('keyframe')
keyFramesAt = []
controllerIdsList = []
fps = int(float(root.attrib['fps']))

# Calculate the frame number by the time parameter of keyframe tag
for i in range(len(keyframes)):
    timeValue = keyframes[i].attrib['time'].split(' ')
    totalFrames = 0
    timeValue = list(filter(None, timeValue))
    if (len(timeValue) > 1):
        timeValue[0] = timeValue[0].replace('s', "")
        totalFrames += int(timeValue[0]) * fps
        timeValue[1] = timeValue[1].replace("f", "")
        totalFrames += int(timeValue[1])
    else:
        if (timeValue[0].find("f") != -1):
            timeValue[0] = timeValue[0].replace('f', "")
            totalFrames += int(timeValue[0])
        else:
            timeValue[0] = timeValue[0].replace('s', "")
            totalFrames += int(timeValue[0]) * fps
    keyFramesAt.append(totalFrames)

exportedDefs = getDefs(root)
for i in range(1, len(keyFramesAt)):
    sliderId = "sliderController" + \
        str(random.randint(1000, 9999)) + "_" + str(keyFramesAt[i])
    controllerIdsList.append(sliderId)
    exportedDefs.append(createReal(value=0, id=sliderId))
    drawSliderUI(root, sliderId)

exportedValues = list(exportedDefs)
exportedDefs.clear()
for ele in reversed(exportedValues):
    exportedDefs.append(ele)

for nodeType in nodeTypes:
    parentsToConnectSlider = []
    for parent in root.findall(f".//*/animated[@type='{nodeType}']/.."):
        animated = parent[0]
        checkList = []
        intialWaypoint = list(animated)[0]
        for waypoint in animated:
            for keyframe in keyFramesAt:
                waypointAtFrame = int(
                    round(float(waypoint.attrib['time'].replace("s", ""))*fps))
                if (waypointAtFrame == keyframe):
                    checkList.append(waypointAtFrame)
        if (checkList == keyFramesAt):
            parentsToConnectSlider.append(parent)
    connectSlider(parentsToConnectSlider, controllerIdsList, nodeType,
                  fps=fps, keyframes = keyFramesAt)

writeTo = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]

with open(writeTo, "wb") as files:
    files.write(minidom.parseString(ElementTree.tostring(
        root, xml_declaration=True)).toxml("utf-8"))
