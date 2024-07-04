using System;
using System.Windows.Forms;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;

namespace Compiler
{
    internal class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                string[] lastIndex = Path.GetFileName(args[0]).Split('.');
                if (lastIndex[lastIndex.Length-1].ToLower() == "ppl")
                {
                    csprojMaker maker = new csprojMaker();
                    csmaker csmaker = new csmaker();
                    string filetext = File.ReadAllText(args[0]);
                    Console.WriteLine("Working with:" + Environment.NewLine + $@"{filetext}");
                    string newfile = $"{lastIndex[lastIndex.Length - 2]}";
                    List<string> csfiles = new List<string>();
                    void comp(string cmdd)
                    {
                        Process cmd = new Process();
                        cmd.StartInfo.FileName = "cmd.exe";
                        cmd.StartInfo.RedirectStandardInput = true;
                        cmd.StartInfo.RedirectStandardOutput = true;
                        cmd.StartInfo.CreateNoWindow = true;
                        cmd.StartInfo.UseShellExecute = false;
                        cmd.Start();
                        cmd.StandardInput.WriteLine(cmdd);
                        cmd.StandardInput.Flush();
                        cmd.StandardInput.Close();
                        cmd.WaitForExit();
                        Console.WriteLine(cmd.StandardOutput.ReadToEnd());
                    }
                    try
                    {
                        Console.WriteLine($"Naming exe as {Path.GetFileNameWithoutExtension(args[1])}");
                        csmaker.BuildCS(args[0], Path.GetFileNameWithoutExtension(args[1]), true);
                        csfiles.Add(args[0].Replace(".ppl", ".cs"));
                        string imports = "nn";
                        while (imports != "")
                        {
                            imports = maker.getBetween(filetext, "import ", " as");
                            if (imports == "") { break; }
                            csmaker.BuildCS(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + imports + ".ppl", args[1], false);
                            csfiles.Add(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + imports + ".cs");
                            filetext = filetext.Replace($"import {imports} as", "");
                        }
                        maker.MakeProj(args[0], csfiles);
                        FileInfo fi = new FileInfo(args[0]);
                        string Full = fi.DirectoryName + "\\" + Path.GetFileNameWithoutExtension(args[1]) + ".csproj";
                        string cmd = $"\"C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe\" \"{Full}\"";
                        comp(cmd);
                    }
                    catch
                    {
                        Console.WriteLine($"Naming exe as {newfile}");
                        csmaker.BuildCS(args[0], newfile, true);
                        csfiles.Add(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + newfile + ".cs");
                        string imports = "nn";
                        while (imports != "")
                        {
                            imports = maker.getBetween(filetext, "import ", " as");
                            if (imports == "") { break; }
                            csmaker.BuildCS(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + imports + ".ppl", newfile, false);
                            csfiles.Add(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + imports + ".cs");
                            filetext = filetext.Replace($"import {imports} as", "");
                        }
                        maker.MakeProj(args[0], csfiles);
                        FileInfo fi = new FileInfo(args[0]);
                        string Full = fi.DirectoryName + "\\" + newfile + ".csproj";
                        string cmd = $"\"C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe\" \"{Full}\"";
                        comp(cmd);
                    }
                    try
                    {
                        if (args[2].ToLower() != "true")
                        {
                            File.Delete(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + args[1] + ".csproj");
                            for (int i = 0; i < csfiles.Count; i++)
                            {
                                File.Delete(csfiles[i]);
                            }
                        }
                    }
                    catch
                    {
                        try
                        {
                            File.Delete(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + args[1] + ".csproj");
                        }
                        catch
                        {
                            File.Delete(Path.GetFullPath(args[0].Replace(Path.GetFileName(args[0]), "")) + newfile + ".csproj");
                        }
                        for (int i = 0; i < csfiles.Count; i++)
                        {
                            File.Delete(csfiles[i]);
                        }
                    }
                    Console.WriteLine("Compilation done!");
                }
                else
                {
                    MessageBox.Show("This file extension can not be compiled via PPL compiler.", "Compiler error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    Environment.Exit(0);
                }
            }
            else
            {
                MessageBox.Show("You must run a *.ppl file via this compiler", "Compiler error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Environment.Exit(0);
            }
        }
    }
}