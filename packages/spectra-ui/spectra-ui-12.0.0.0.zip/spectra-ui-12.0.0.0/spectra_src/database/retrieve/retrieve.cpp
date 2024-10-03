#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <iomanip>

#include "common.h"

using namespace std;

#define MAXZ 92

void dump_items(ofstream &ss, int Zrange[], vector<vector<double>> &variable, vector<vector<double>> &items)
{
	int nmax = 0;
	for(int Z = Zrange[0]; Z <= Zrange[1]; Z++){
		if(Z > Zrange[0]){
			ss << "\t";
		}
		ss << "E" << Z << "\t" << "r" << Z;
		nmax = max(nmax, (int)variable[Z].size());
	}
	ss << endl;
	for(int n = 0; n < nmax; n++){
		for (int Z = Zrange[0]; Z <= Zrange[1]; Z++){
			if (Z > Zrange[0]){
				ss << "\t";
			}
			if(variable[Z].size() <= n){
				ss << "-" << "\t" << "-";
			}
			else{
				ss << variable[Z][n] << "\t" << items[Z][n];
			}
		}
		ss << endl;
	}
}

void print_items(string caption, ofstream &ss, vector<vector<double>> &items)
{
	ss << "const vector<vector<double>> ";
	ss << caption;
	ss << " {\n";
	for(int Z = 0; Z <= MAXZ; Z++){
		ss << "    vector<double> {";
		for(int n = 0; n < items[Z].size(); n++){
			if(n > 0){
				ss << ", ";
			}
			if(n%10 == 0 && n > 0){
				ss << endl;
				ss << "                ";
			}
			ss << items[Z][n];
		}
		ss << "}";
		if(Z < MAXZ){
			ss << ",";
		}
		ss << endl;
	}
	ss <<  "};" << endl;
}

int main()
{
	string filename;
	stringstream sd;
	vector<vector<double>> energies(MAXZ+1), ratios(MAXZ+1);
	for(int Z = 1; Z <= MAXZ; Z++){
		sd << setfill('0') << setw(2);
		sd << Z;
		filename = "z"+sd.str()+".txt";
		sd.str("");
		sd.clear(stringstream::goodbit);

		ifstream ifs(filename);
		if(!ifs){
			cout << "error at" << filename;
		}
		string input = string((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
		ifs.close();

		vector<string> lines, items;
		int nlines =  separate_items(input, lines, "\n", false);
		int iline = 0, nitems;
		vector<double> energy, ratio;
		char *endp;

		while(lines[iline++].find("<PRE>") == string::npos);
		while(1){
			if(lines[iline++].find("</PRE>") != string::npos){
				break;
			}
			trim(lines[iline]);
			nitems = separate_items(lines[iline], items, " ", true);
			if(nitems < 3){
				continue;
			}
			for(int j = 0; j  < nitems; j++){
				trim(items[j]);
			}
			int i0 = 0;
			if(nitems == 4){
				i0 = 1;
			}
			double values[3];
			bool isok = true;
			for(int j = 0; j < 3; j++){
				values[j] = strtod(items[j+i0].c_str(), &endp);
				if(items[j+i0] == string(endp)){
					isok = false;
					break;
				}
			}
			if(!isok){
				continue;
			}
			values[0] *= 1e6; // MeV -> eV
			if(energy.size() > 0){
				if(energy.back() == values[0]){
					values[0] += 1;
					// avoid over lap, 1eV shift
				}
			}
			energy.push_back(values[0]);
			ratio.push_back(values[2]/values[1]);
		};
		energies[Z] = energy;
		ratios[Z] = ratio;
	}
	energies[0] = vector<double> {};
	ratios[0] = vector<double> {};

	int Zrange[2] = {1, 10};
	int dZ = 10;
	for(int ZZ = 1; ZZ <= MAXZ; ZZ += dZ){
		Zrange[0] = ZZ;
		Zrange[1] = min(MAXZ, ZZ+dZ-1);
		stringstream fss;
		fss << "chk" << Zrange[0] << "-" << Zrange[1] << ".dat";
		ofstream ofs(fss.str());
		dump_items(ofs, Zrange, energies, ratios);
	}

	ofstream ss("..\\energy_absorption_ratio.h");
	ss << "#ifndef energy_absorption_ratio_h" << endl;
	ss << "#define energy_absorption_ratio_h" << endl;
	ss << "#include <vector>" << endl << endl;
	ss << "using namespace std;" << endl << endl;
	print_items("tbl_energies", ss, energies);
	ss << endl;
	print_items("tbl_ratios", ss, ratios);
	ss << "#endif" << endl;
	
}
