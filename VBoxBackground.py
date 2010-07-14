#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk
import os

class VBoxBackground:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(10)
        self.window.set_title("VBoxBackground")

        self.container = gtk.HBox()
        self.subcontainer_a = gtk.VBox()
        self.subcontainer_b = gtk.VBox()

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.start_button = gtk.Button("Start")
        self.start_button.connect("clicked", self.start_vm)

        self.stop_button = gtk.Button("PowerOFF")
        self.stop_button.connect("clicked", self.poweroff_vm)

        self.savestate_button = gtk.Button("Save State")
        self.savestate_button.connect("clicked", self.savestate_vm)

        self.combobox = gtk.combo_box_new_text()
        self.vms()

        self.subcontainer_a.add(self.start_button)
        self.subcontainer_a.add(self.savestate_button)
        self.subcontainer_a.add(self.stop_button)
        self.subcontainer_b.add(self.combobox)

        self.container.add(self.subcontainer_a)
        self.container.add(self.subcontainer_b)

        self.window.add(self.container)
        self.window.show_all()

    def start_vm(self, widget):
        os.popen("VBoxManage startvm " + self.vm_atual() + " --type=vrdp")
        self.change_status("on")
        print "Starting VM " + self.vm_atual()

    def savestate_vm(self, widget):
        os.popen("VBoxManage controlvm " + self.vm_atual() + " savestate")
        self.change_status("salved")
        print "Salvando status VM " + self.vm_atual()

    def poweroff_vm(self, widget):
        os.popen("VBoxManage controlvm " + self.vm_atual() + " poweroff")
        self.change_status("off")
        print "Stoping VM " + self.vm_atual()

    def delete_event(self, widget, event, data=None):
        return False

    def vms(self):
        lista = os.popen("VBoxManage list vms").readlines()
        for i,x in enumerate(lista):
            if i>3 :
                name = x.split('"')[1]
                name = name + " ["+ self.vm_state(name) + "]"
                self.combobox.append_text(name)

    def runningvms(self):
        lista = os.popen("VBoxManage list runningvms").readlines()
        l = []
        for i,x in enumerate(lista):
            if i>3 :
                l.append(x.split('"')[1])
        return l

    def vm_atual(self):
        return self.combobox.get_model()[self.combobox.get_active()][0].split(" ")[0]

    def vm_state(self,name):
        status = os.popen("VBoxManage showvminfo " + name + " | grep 'State:'").readlines()[0]
        status = status.split("State:           ")[1].split(" (")[0]
        if status == "running":
            return "on"
        elif(status=="saved"):
            return "saved"
        else:
            return "off"

    def vm_info(self,name):
        return  os.popen("VBoxManage showvminfo " + name + "").readlines()

    def change_status(self,tipo):
        self.combobox.get_model()[self.combobox.get_active()][0] = self.vm_atual() + " [" + tipo+"]"

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    vboxb = VBoxBackground()
    vboxb.main()

