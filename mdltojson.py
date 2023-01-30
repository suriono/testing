#testing branch again

import re, sys

argv=sys.argv[1:len(sys.argv)]


########### MDL class ##############################

#global Models

class MDL_File:
   Model = {}
   def __init__(self, name):
      self.name = name
class MDL_Model:
   DUTs = {}
   Temp = None
   Variables = {}
   def __init__(self, name):
      self.name = name
class MDL_DUT:
   Setups = {}
   Temp = None
   Variables = {}
   title = ''
   def __init__(self, name):
      self.name = name
class MDL_SETUP:
   Temp = None
   Variables = {}
   Sweeps   = {}
   Outputs  = {}
   Report_Plots = []
   RMSxlow  = None
   RMSxhigh = None
   RMSylow  = None
   RMSyhigh = None
   def __init__(self, name):
      self.name = name
class MDL_Plot:
   Sweep   = {}
   Outputs  = {}
   title = ''
class MDL_Sweep:
   type  = ''
   order  = 1
   start = ''
   stop  = -2
   listsweep  = []
   title = ''
   pts   = 0
   stepsize = 0
   def __init__(self, name):
      self.name = name
class MDL_Output:
   meas = []
   sim  = []
   xform  = []
   type = ''
   yscale= ''
   matrix_size = 0
   def __init__(self, name):
      self.name = name

class PLOT:
   Filename = ''
   DUT = ''

class VAR:
   name = ''
   value = ''
   def __init__(self, name):
      self.name = name

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

########### Read Device Config file ##############################

def Read_Device_Config_file(filen, Config):
   filen = filen.replace("\"","")
   print "\tReading device config file: ", filen
  
   try:
      filecon = open(filen, "r")
   except:
      print "\n   Cannot read file: ", filen
      sys.exit(0)

   line = filecon.readline()
   while len(line):
      line = line.strip().replace("'","")
      line = line.replace("\"","")
      if (re.search(",", line)):
         tmparr = line.split(",")
         Config[tmparr[0]] = tmparr[1]
    
      line = filecon.readline().strip().replace("'","")
      line = line.replace("\"","")
   filecon.close()

# --------- End of Device Config file ---------------------------

########### Read MDL Config file ##############################

def File_Indent (ntimes):
   indent_str = ""
   for nn in range(0, ntimes):
      indent_str += "   "
   return indent_str

def Read_MDL_Config_file ():
#   global Models
   Config = {}
#   Models = {}
   Indent_level = 0

   outfilename = "data.json"

   Mdl_files = {}   # reading mdl_report_config.csv file
   modeltitle = ""

   print "Reading mdl_report_config.csv file ...."
   try:
      fileconf = open("mdl_report_config.csv", "r")
   except:
      print "\n   Cannot read file: mdl_report_config.csv"
      sys.exit(0)


   line = fileconf.readline().strip().replace("'","")
   line = line.replace("\"","")
   if len(line):
      headers = line.split(",")
      line = fileconf.readline().strip().replace("'","")
      line = line.replace("\"","")

      fileout = open(outfilename, "w")

      while len(line) and line.find(",") >= 0:

         line = line.strip().replace("'","")
         line = line.replace("\"","")
         if re.search('[\w]+', line) == None:
            line = fileconf.readline()
            continue

         tmparr = line.strip().split(",")

         if len(tmparr[headers.index('CONFIG')]):
            config_file = tmparr[headers.index('CONFIG')]
            Read_Device_Config_file(config_file, Config)
            filename = Config['MDL']
            #filename = argv[0]

            print "\tReading MDL file: ", filename
            Read_MDL_file ( filename )
            fileout.write ("[\n")
            Indent_level = 0

         if len(tmparr[headers.index('MODEL')]): modelname = tmparr[headers.index('MODEL')]

         if len(tmparr[headers.index('MODEL-TITLE')]):
            modeltitle = tmparr[headers.index('MODEL-TITLE')]
#            fileout.write ("{\n" + File_Indent(1) + "\"DEVICE\":\"" + modeltitle + "\",\n")
#            fileout.write(File_Indent(1) + "\"PLOTS\": [\n")

         if len(tmparr[headers.index('DUT')]):
            try:
               dutname
               fileout.write(File_Indent(1) + "]\n\n},\n")       # start another DUT
            except:
               pass                                              # the very first DUT
            dutname = tmparr[headers.index('DUT')]

            is_first_plot_of_dut = True;

         if len(tmparr[headers.index('DUT-TITLE')]):
            duttitle = tmparr[headers.index('DUT-TITLE')]
            fileout.write ("{\n" + File_Indent(1) + "\"DUT\":\"" + duttitle + "\",\n")
            if len(modeltitle):
               fileout.write (File_Indent(1) + "\"DEVICE\":\"" + modeltitle + "\",\n")
               modeltitle = ""
            fileout.write(File_Indent(1) + "\"PLOTS\": [\n")

         if len(tmparr[headers.index('SETUP')]): setupname = tmparr[headers.index('SETUP')]

         if len(tmparr[headers.index('SWEEP')]):
            sweepname = tmparr[headers.index('SWEEP')]

            if (is_first_plot_of_dut):
               is_first_plot_of_dut = False;
            else:
               fileout.write (File_Indent(2) + ",\n")
            fileout.write (File_Indent(2) + "{\n")   # for the first plot of DUT

         if len(tmparr[headers.index('OUTPUT')]): outputs = tmparr[headers.index('OUTPUT')]

         if len(tmparr[headers.index('XSCALE')]): xscale = tmparr[headers.index('XSCALE')]

         if len(tmparr[headers.index('YSCALE')]): yscale = tmparr[headers.index('YSCALE')]

         if len(tmparr[headers.index('TITLE')]): titleplot = tmparr[headers.index('TITLE')]

         # if len(tmparr[headers.index('OPTIONS')]): options = tmparr[headers.index('OPTIONS')]
         try:
            tmparr[headers.index('OPTIONS')]
            options = tmparr[headers.index('OPTIONS')]
         except:
            options = ""


         # --- start writing data JSON -----------
         mdlsetup = Models[modelname].DUTs[dutname].Setups[setupname]

         fileout.write (File_Indent(3) + "\"format-version\":1,\n")
         fileout.write (File_Indent(3) + "\"device\":\"" + Config['DEVICE'] + "\",\n")
         fileout.write (File_Indent(3) + "\"title\":\"" + titleplot + "\",\n")
         fileout.write (File_Indent(3) + "\"options\":\"" + options + "\",\n")
         fileout.write (File_Indent(3) + "\"data\":  {\n")

         temperature = "25"
         if Models[modelname].DUTs[dutname].Setups[setupname].Temp:
            temperature = Models[modelname].DUTs[dutname].Setups[setupname].Temp
         elif Models[modelname].DUTs[dutname].Temp:
            temperature = Models[modelname].DUTs[dutname].Temp
         elif Models[modelname].Temp:
            temperature = Models[modelname].Temp
         fileout.write (File_Indent(4) + "\"temperature\": \"" + temperature + "\",\n")
         fileout.write (File_Indent(4) + "\"Batch\": \"" + Config['BATCH'] + "\",\n")
         fileout.write (File_Indent(4) + "\"Wafer\": \"" + Config['WAFER'] + "\",\n")
         fileout.write (File_Indent(4) + "\"Die\": \"" + Config['DIE'] + "\",\n")

#         if mdlsetup.RMSxlow:  fileout.write ("\n            \"RMSxlow\":"  + Unit_Conversion(mdlsetup.RMSxlow) + ",")
#         if mdlsetup.RMSxhigh: fileout.write ("\"RMSxhigh\":" + Unit_Conversion(mdlsetup.RMSxhigh) + ",")
#         if mdlsetup.RMSylow:  fileout.write ("\n            \"RMSylow\":"  + Unit_Conversion(mdlsetup.RMSylow) + ",")
#         if mdlsetup.RMSyhigh: fileout.write ("\"RMSyhigh\":" + Unit_Conversion(mdlsetup.RMSyhigh) + ",")

         if len(xscale): fileout.write (File_Indent(4) + "\"leftXscale\": \"" + xscale + "\",\n")
         if len(yscale): fileout.write (File_Indent(4) + "\"leftYscale\": \"" + yscale + "\",\n")
         fileout.write (File_Indent(4) + "\"leftYlabel\": \"" + outputs.replace('&', ' & ') + "\",\n")
         fileout.write (File_Indent(4) + "\"cols\":  [\n")
         fileout.write (File_Indent(5) + "{ \"label\": \"" + sweepname + "\",\"type\":\"number\"}")


         try:
            mdlsetup.Sweeps[re.sub("-", "", sweepname)]
            sweepvalues = Create_Sweep(mdlsetup.Sweeps[re.sub("-", "", sweepname)], sweepname, setupname, dutname, modelname)
         except:
#           try: 
            mdlsetup.Outputs[re.sub("-", "", sweepname)]
            sweepvalues = mdlsetup.Outputs[re.sub("-", "", sweepname)].meas
#            except:
#               sys.exit("\n\n\t\tError reading sweep: " + modelname + "/" + dutname + "/" + sweepname + "\n\n")

         second_order_sweep = ''
         secondordersweepvalues = []
         for eachsweep in mdlsetup.Sweeps:
            if int(mdlsetup.Sweeps[eachsweep].order) == 2 and int(mdlsetup.Sweeps[eachsweep].pts) > 1:  # if there is a 2nd order sweep
               second_order_sweep = eachsweep
#               print "=============", eachsweep, mdlsetup.Sweeps[eachsweep].pts
               secondordersweepvalues = Create_Sweep(mdlsetup.Sweeps[eachsweep], eachsweep, setupname, dutname, modelname)
                

         output_signs = []
         output_nosigns = []
         outputs_items = outputs.split("&")


       
         # writing the labels cols
         for eachout in outputs_items:		# each OUTPUT from mdl_report_config.csv file
            if re.match('-', eachout): 
               output_signs.append(-1.0)
            else:
               output_signs.append(1.0)
            
            outname = re.sub("-","", eachout)
            #output_nosigns.append(re.sub("-","", eachout))   # removing any negative output name
            output_nosigns.append(outname)   # removing any negative output name


 	    try:		# check if it's not an array of number but could be array of table values
               len(mdlsetup.Outputs[outname].meas)

               if len(mdlsetup.Outputs[outname].meas) > 0:
                  for ncurve in range(0, len(mdlsetup.Outputs[outname].meas) / len(sweepvalues) ):
                     fileout.write (",\n" + File_Indent(5) + "{ \"label\": \"" + eachout + "(meas)")
                     if len(second_order_sweep): fileout.write (" @" + second_order_sweep + "=")
                     if len(second_order_sweep): fileout.write (str(secondordersweepvalues[ncurve]))
               
                     fileout.write ("\",\"type\":\"number\"},\n")
                     fileout.write (File_Indent(5) + "{ \"label\": \"" + eachout + "(sim)\",\"type\":\"number\"}")
               else:
                  fileout.write (",\n" + File_Indent(5) + "{ \"label\": \"" + eachout)
                  fileout.write ("\",\"type\":\"number\"}")

            except KeyError:		# table values at this point

#               print mdlsetup.Variables[outname].name
               fileout.write (",\n" + File_Indent(5) + "{ \"label\": \"" + mdlsetup.Variables[outname].name)
               fileout.write ("\",\"type\":\"string\"}")

            except:
               print "Unexpected error:", sys.exc_info()[0]
               raise


         # rows of data
         fileout.write ("],\n" + File_Indent(4) + "\"rows\":  [\n")


         nn = -1
         for eachsweep in sweepvalues:
            nn = nn + 1
            if re.match('log', xscale):
               fileout.write(File_Indent(5) + "{\"c\":[ {\"v\":%.6e} " % abs(eachsweep))
            else:
               fileout.write(File_Indent(5) + "{\"c\":[ {\"v\":%.6e} " % eachsweep)

            for nout in range(0, len(outputs_items)):

               sign_output = output_signs[nout]
               out_no_sign = output_nosigns[nout]   # removing any negative output name
           

               try:      # if the output is numeric, not a table for example
                  len(mdlsetup.Outputs[output_nosigns[nout]].meas)

                  if len(mdlsetup.Outputs[output_nosigns[nout]].meas) > 0:
                     for ncurve in range(0, len(mdlsetup.Outputs[output_nosigns[nout]].meas) / len(sweepvalues) ):
                        nindex = ncurve * len(sweepvalues) + nn
                        fileout.write(",{\"v\":%.6e}" % (sign_output*mdlsetup.Outputs[out_no_sign].meas[nindex]))
                        fileout.write(",{\"v\":%.6e} " % (sign_output*mdlsetup.Outputs[out_no_sign].sim[nindex]))
                  else:  # for transform without meas and sim pair
                     for ncurve in range(0, len(mdlsetup.Outputs[output_nosigns[nout]].xform) / len(sweepvalues) ):
                        nindex = ncurve * len(sweepvalues) + nn
                        fileout.write(",{\"v\":%.6e}" % (sign_output*mdlsetup.Outputs[out_no_sign].xform[nindex]))

               except KeyError:     # for table at this point
#                  print mdlsetup.Variables[out_no_sign].name
                  #print mdlsetup.Variables[out_no_sign + "[" + nn + "]"].value
#                  print mdlsetup.Variables[out_no_sign + "[" + str(nn) + "]"].name
#                  print mdlsetup.Variables[out_no_sign + "[" + str(nn) + "]"].value
                  fileout.write(",{\"v\":\"%s\"}" % ( mdlsetup.Variables[out_no_sign + "[" + str(nn) + "]"].value ))

               except:
                  print "Unexpected error:", sys.exc_info()[0]
                  raise



            if nn < len(sweepvalues)-1:  # pop data until nothing left
               fileout.write(" ]},\n")
            else:
               fileout.write(" ]}  ]\n")

         fileout.write("\n" + File_Indent(3) + "}\n")
         fileout.write(File_Indent(2) + "}\n\n")      # end of each plot

         line = fileconf.readline()
#         line = fileconf.readline().strip().replace("'","")

   fileout.write("]\n\n}")              # end of multiple plots each DUT
   fileout.write ("]\n")
   fileout.close()



# ------- End of Read_MDL_Config_file ---------------------


########### Read MDL file ##############################

def Read_MDL_file ( mdl_filename ):

   global Models
   Models = {}
#    mdl_filename = sys.argv[1]
   try:
      fileopen = open(mdl_filename, "r")
   except:
      print "\n   Cannot read file: ", mdl_filename
      sys.exit(0)

   line = fileopen.readline()
   while len(line):

      if re.match ('LINK MODEL ', line):
         level = 0
         modelname = re.search('\"' + "(.*)" + "\".*\".*\"", line).group(1)
         Models[modelname] = MDL_Model(modelname)
         Models[modelname].DUTs = {}

      elif re.match ('{', line):
         Read_file_recursive (Models[modelname], fileopen, 0)


      line = fileopen.readline()
   fileopen.close()
   return Models

########### Read MDL file recurcively ##############################

def Read_file_recursive (iccap_struct, fileopen, level):
   level = level + 1
   next_struct = {}
   line = fileopen.readline()

   while len(line):
      if re.match ('{', line):
          Read_file_recursive (next_struct, fileopen, level)
      elif re.match ('}', line):
         return
#      elif re.match ('TABLE "Variable Table" ', line):
#         print "==== table variable: ", level
      elif re.match ('LINK DUT ', line):
         dutname = re.search('\"' + "(.*)" + "\".*\".*\"", line).group(1)
         iccap_struct.DUTs[dutname] = MDL_DUT(dutname)
         iccap_struct.DUTs[dutname].Setups = {}
         next_struct = iccap_struct.DUTs[dutname]
      elif re.match ('LINK DAT ', line):
         setupname = re.search('\"' + "(.*)" + "\".*\".*\"", line).group(1)
         iccap_struct.Setups[setupname] = MDL_SETUP(setupname)
         iccap_struct.Setups[setupname].Sweeps = {}
         iccap_struct.Setups[setupname].Outputs = {}
         next_struct = iccap_struct.Setups[setupname] 
      elif re.match ('LINK SWEEP ', line):
         sweepname = re.search('\"' + "(.*)" + "\".*\".*\"", line).group(1)
         iccap_struct.Sweeps[sweepname] = MDL_Sweep(sweepname)
         iccap_struct.Sweeps[sweepname].listsweep = []
         next_struct = iccap_struct.Sweeps[sweepname] 
      elif re.match ('element "Sweep Type" ', line):
         sweeptype = re.search('Type\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.type = sweeptype
      elif re.match ('element "Sweep Order" ', line):
         sweeporder = re.search('Order\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.order = sweeporder
      elif re.match ('element "Start" ', line):
         sweepstart = re.search('Start\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.start = sweepstart
      elif re.match ('element "Stop" ', line):
         sweepstop = re.search('Stop\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.stop = sweepstop
      elif re.match ('element "# of Points" ', line):
         pts = re.search('Points\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.pts = pts
      elif re.match ('element "Total Pts" ', line):
         pts = re.search('Pts\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.pts = pts
#         print "======= pts: ", pts, level
      elif re.match ('element "Step Size" ', line):
         stsize = re.search('Step Size\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.stepsize = stsize
      elif re.match ('element "# of Values" ', line):
         pts = re.search('Values\"\s\"' + "(.*)" + "\"", line).group(1)
         iccap_struct.pts = pts
#         print "======= pts: ", pts, level
      elif re.match ('element "Value' , line) and iccap_struct.type == 'LIST':
         value =  re.search('Value ' + "(\d+)\" \"" + "(.*)" + "\"" , line).group(2)
#         print "=======sweep list ====", level,iccap_struct.name, line
#         print "\t", value
         iccap_struct.listsweep.append(value)
      elif re.match ('LINK OUT ', line):
         outname = re.search('\"' + "(.*)" + "\".*\".*\"", line).group(1)
         iccap_struct.Outputs[outname] = MDL_Output(outname)
         iccap_struct.Outputs[outname].type = 'OUT'
         next_struct = iccap_struct.Outputs[outname] 
      elif re.match ('LINK XFORM ', line):
         outname = re.search('\"' + "(.*)" + "\".*\".*\"", line).group(1)
         iccap_struct.Outputs[outname] = MDL_Output(outname)
         iccap_struct.Outputs[outname].type = 'XFORM'
         next_struct = iccap_struct.Outputs[outname] 
      elif re.search ('element ' + "(\d+)" + " \"Name\" \"X_LOW\"" , line) and level == 4:
         line = fileopen.readline()
         iccap_struct.RMSxlow = re.search("Value\" \"" + "(.*?)" + "\"", line).group(1)
      elif re.search ('element ' + "(\d+)" + " \"Name\" \"X_HIGH\"" , line) and level == 4:
         line = fileopen.readline()
         iccap_struct.RMSxhigh = re.search("Value\" \"" + "(.*?)" + "\"", line).group(1)
      elif re.search ('element ' + "(\d+)" + " \"Name\" \"Y_LOW\"" , line) and level == 4:
         line = fileopen.readline()
         iccap_struct.RMSylow = re.search("Value\" \"" + "(.*?)" + "\"", line).group(1)
      elif re.search ('element ' + "(\d+)" + " \"Name\" \"Y_HIGH\"" , line) and level == 4:
         line = fileopen.readline()
         iccap_struct.RMSyhigh = re.search("Value\" \"" + "(.*?)" + "\"", line).group(1)
      elif re.search ('element ' + "(\d+)" + " \"Name\" \"TEMP\"" , line):
         line = fileopen.readline()
         iccap_struct.Temp = re.search("Value\" \"" + "(.*?)" + "\"", line).group(1)
      elif re.search ('element ' + "(\d+)" + " \"Name\" " , line):         # table variables 
         name = re.search("Name\" \"" + "(.*?)" + "\"", line).group(1) 
         line = fileopen.readline()
         try:
            re.search("Value\" \"" + "(.*?)" + "\"", line).group(1)
            iccap_struct.Variables[name] = VAR(name)
            iccap_struct.Variables[name].value = re.search("Value\" \"" + "(.*?)" + "\"", line).group(1)

#            print "==== table variable: ", level, "Name: ", iccap_struct.Variables[name].name, " , Value: ", iccap_struct.Variables[name].value
         
         except:
            pass


      elif re.match ('datasize BOTH', line):
         iccap_struct.meas = []
         iccap_struct.sim = []
         tmpstr = line.strip().split(" ")
         iccap_struct.matrix_size = int(tmpstr[3]) * int(tmpstr[4])
         if re.match ('type MEAS', fileopen.readline()):
            line = fileopen.readline()
            while re.match ('point ', line):
               tmpstr = line.split(" ")
               iccap_struct.meas.append(float(tmpstr[4]))
               line = fileopen.readline()
         if re.match ('type SIMU', line):
            line = fileopen.readline()
            while re.match ('point ', line):
               tmpstr = line.split(" ")
               iccap_struct.sim.append(float(tmpstr[4]))
               line = fileopen.readline()
#            print "\t\t\t\tSimu: ", iccap_struct.meas
         continue


      elif re.match ('datasize COMMON', line):  # XFORM with no simulated
         iccap_struct.meas = []
         iccap_struct.xform = []
         tmpstr = line.strip().split(" ")
         iccap_struct.matrix_size = int(tmpstr[3]) * int(tmpstr[4])
         line = fileopen.readline()
         if int(tmpstr[2]) > 0:
            line = fileopen.readline()
            while re.match ('point ', line):
               tmpstr = line.split(" ")
               iccap_struct.xform.append(float(tmpstr[4]))
               line = fileopen.readline()
#            if re.match('Length', iccap_struct.name):
#               for eachitem in iccap_struct.xform:
#                  print "------ ", eachitem, iccap_struct.name
#               print " =================================="

         continue

      else:
         next_struct = iccap_struct


      line = fileopen.readline()
      

# ------- End of Read MDL file ---------------------

# ====================== Number unit conversion e.g. m, n, MEG, k, u, f ================

def Unit_Conversion (newstr, setupname, dutname, modelname):
   teststr = newstr
   teststr = re.sub("m", "E-3",  teststr)
   teststr = re.sub("u", "E-6",  teststr)
   teststr = re.sub("n", "E-9",  teststr)
   teststr = re.sub("p", "E-12", teststr)
   teststr = re.sub("f", "E-15", teststr)
   teststr = re.sub("a", "E-18", teststr)

   if Is_a_Number(teststr):
#      print "=== IS a number ===== "
      return teststr
   else:
#      print "====================uzzz ", newstr
#      print "=== NOT a number ===== "
#      varlist = re.findall('[+-/*//()]|[0-9a-zA-Z\.E-e-]+',newstr)   # finding math operator
#      varlist = re.findall('[+-/*//()]|[0-9a-zA-Z\.]+|[0-9E+-]+',newstr)   # finding math operator
      varlist = re.findall('[+-/*//()]|[_0-9a-zA-Z\.]+|[0-9E+-]+',newstr)   # finding math operator
#      print "=== NOT a number ===== ", varlist
      
      # variable substitution
      equationstr = ''
      for eachitem in varlist:
         eachvalue = eachitem
         if Is_a_Number(eachitem):
            eachvalue = eachitem
         else:
#            print " Not a number: ", eachitem
            try:
               Models[modelname].DUTs[dutname].Setups[setupname].Variables[eachitem]
#               print " setup variable: ", eachitem
               eachvalue = Models[modelname].DUTs[dutname].Setups[setupname].Variables[eachitem].value
            except:
               try:
                  Models[modelname].DUTs[dutname].Variables[eachitem]
#                  print " dut variable: ", eachitem
                  eachvalue = Models[modelname].DUTs[dutname].Variables[eachitem].value
               except:
                  try:
                     Models[modelname].Variables[eachitem]
#                     print " model variable: ", eachitem , " Value: ", Models[modelname].Variables[eachitem].value
                     eachvalue = Models[modelname].Variables[eachitem].value
                  except:
                     pass
         eachvalue = re.sub("m", "E-3",  eachvalue)
         eachvalue = re.sub("u", "E-6",  eachvalue)
         eachvalue = re.sub("n", "E-9",  eachvalue)
         eachvalue = re.sub("p", "E-12", eachvalue)
         eachvalue = re.sub("f", "E-15", eachvalue)
         eachvalue = re.sub("a", "E-18", eachvalue)
         equationstr += eachvalue

#      print " eq: ", equationstr, " = " , str(eval(equationstr))
      return equationstr
            

# ================== Check if it's a number ===========================
def Is_a_Number(numstr):
   try:
      float(numstr)
      return True
   except:
      return False

# ====================== Build a sweep array from sweep information ================

def Create_Sweep(sweep, sweepname, setupname, dutname, modelname):
   tmparr = []
#   pts   = int(sweep.pts)
#   print "============", Unit_Conversion(str(sweep.pts), setupname, dutname, modelname)
   pts   = int(eval(Unit_Conversion(str(sweep.pts), setupname, dutname, modelname)))
#   print "============", pts
#   print "======", sweepname, pts, Models[modelname].DUTs[dutname].Setups[setupname].Sweeps[sweep.name].type

#   sweeptype = Models[modelname].DUTs[dutname].Setups[setupname].Sweeps[sweepname].type
   sign = 1.0
   if re.match('-', sweepname):
      sign = -1.0

   if sweep.type == 'LIN':
      stsize = float(eval(Unit_Conversion(sweep.stepsize, setupname, dutname, modelname)))
      start = float(eval(Unit_Conversion(sweep.start, setupname, dutname, modelname)))
#      print "============", sweep.stepsize, stsize,  start, sweep.stop, Unit_Conversion(sweep.stop , setupname, dutname, modelname)
      stop  = float(eval(Unit_Conversion(sweep.stop , setupname, dutname, modelname)))


      if pts < 1:
         pts = int (round((stop - start)/stsize, 0)) + 1

 
      for i in range(0, pts):
         tmparr.append((start + i*(stop - start)/(pts-1)) * sign)
   elif sweep.type == 'LIST':
#      print "=============", sweep.type, sweep.name
#      print "======----", len(Models[modelname].DUTs[dutname].Setups[setupname].Sweeps[sweep.name].listsweep)
#      print "======----", Models[modelname].DUTs[dutname].Setups[setupname].name
      for eachitem in Models[modelname].DUTs[dutname].Setups[setupname].Sweeps[sweep.name].listsweep:
#         print "=============", eachitem
         value = float(eval(Unit_Conversion( eachitem, setupname, dutname, modelname)))
         tmparr.append(value * sign)
#         print "=============", eachitem, " = ", value
#         print "=============", eachitem
#      print Models[modelname].DUTs[dutname].Setups[setupname].Sweeps[sweepname].list
#      sys.exit()
   elif sweep.type == 'LOG':
      start = float(eval(Unit_Conversion(sweep.start, setupname, dutname, modelname)))
      stop  = float(eval(Unit_Conversion(sweep.stop , setupname, dutname, modelname)))
      stsize = (stop / start)**(1.0/(pts-1))
#      print "======", pts, start, stop, stsize
      for i in range(0, pts):
         tmparr.append((start * (stop/start)**(i/(pts-1.0))) * sign)
#         print (start * (stop/start)**(i/(pts-1.0))) * sign

#      print "\n\n\t ERROR: Not eep type: ", sweep.type, "\n\n"
   else:
      print "\n\n\t ERROR: Not implemented yet, sweep type: ", sweep.type, "\n\n"
      sys.exit()





   return tmparr

# ============================================================================

# when used stand alone
if (len(argv) < 1):
   Read_MDL_Config_file ()
#else:
#   print "\n\n\tNote: to generate JSON file (data.json):\n"
#   print "\t\tpython mdltojson.py <MDL file name>\n\n";
   

