#ifndef hermite_gauss_decomp_h
#define hermite_gauss_decomp_h

#include <complex>
#include "wigner4d_manipulator.h"
#include "optimization.h"
#include "quadrature.h"
#include "fast_fourier_transform.h"
#include "print_calculation_status.h"

using namespace std;

class HermiteGaussianMode
{
public:
	HermiteGaussianMode(double sigma, double lambda, int maxorder);
	double GetField(int mode, double x);
	void GetWigner(int n, int m, double x, double theta, double *W);
	double HGFunc(int mode, double xh);
	double LGFunc(int n, int m, double r);

private:
	vector<double> m_hgcoef;
	vector<vector<double>> m_lgcoef;
	vector<vector<bool>> m_alloc;

	double m_sigma;
	double m_lambda;
	int m_maxorder;
};

class HGModalDecomp
	: public SearchMinimum, public QSimpson
{
public:
	HGModalDecomp(int layer, PrintCalculationStatus *calcstatus, 
		int acclevel, int kmax, double cutoff, double fluxcut, Wigner4DManipulator *wig4d);
	~HGModalDecomp();
	void LoadData();
	bool AssingData(vector<vector<double>> *xyqarr, vector<vector<double>> &data, bool isstat);
	void SetBeamParameters();
	void OptimizeSrcSize(double *defsrcsize = nullptr, int *layer = nullptr);
	void FourierExpansionSingle(double rh, int kmax, vector<double> *fr, vector<double> *fi);
	void FourierExpansion();
	void CreateHGMode(double *norm = nullptr);

	int GetIntegrateRange(vector<vector<double>> &rrange, bool forcedebug = false);
	void GetAnm(vector<vector<complex<double>>> *Anm = nullptr, 
		int rank = 0, int mpiprocesses = 1, bool forcedebug = false);
    virtual double CostFunc(double x, vector<double> *y);
	virtual void QSimpsonIntegrand(int layer, double rh, vector<double> *density);

	void SetAnm(vector<vector<complex<double>>> *Anm);
	double CholeskyDecomp(vector<vector<complex<double>>> *anm = nullptr, vector<int> *order = nullptr);
	void Get_anm(vector<vector<complex<double>>> &anm);
	void Set_anm(vector<vector<complex<double>>> &anm);
	complex<double> GetComplexAmpSingle(int mode, double eps, double xh);
	void GetComplexAmp(vector<double> &xyarr,
			vector<vector<complex<double>>> *Ea, double eps, int pmax, bool issimple = false, bool skipstep = false);
	void GetApproximatedAnm(int pmax, double eps, 
		vector<complex<double>> *aAnm, vector<int> *nindex, vector<int> *mindex);
	void GetFluxConsistency(int pmax, double eps, vector<double> &fr, vector<double> &fa);
	void ReconstructExport(
		int pmax, double epsanm, double *CMDerr, vector<double> &data, int rank = 0, int mpiprocesses = 1);
	void GetWignerAt(int pmax, double eps,
		double xy, double dq, int hqmesh, vector<double> &W);

	void SetGSModel();

	void SetMaximumModeNumber(int mode){m_maxmodenumber = mode;}
	void SetNormalization(double nf){m_norm_factor = nf;}
	double GetNormalization(){return m_norm_factor;}
	double GetSigma(){return m_srcsize;}
	void SetSigma(double srcsize){m_srcsize = srcsize;}
	HermiteGaussianMode *GetHGMode(){return m_hgmode;}
	int GetMaxOrder(int pmax);

	void DumpFieldProfile(const char *bufbin, 
		double eps, int pmax, double dxy, bool iswrite, 
		vector<double> &xyarr, vector<vector<double>> &datar, vector<vector<double>> &datai);
	void WriteResults(string &result, double cmderr[]);
	void LoadResults(int maxorder, double srcsize, 
		double fnorm, vector<double> &anmre, vector<double> &anmim);

private:
	void f_SetupDataGrid(double *ladj = nullptr);
	void f_AssignWignerArray(vector<vector<complex<double>>> *ws, 
			vector<double> *xyarr, vector<double> *qarr);
	void f_ComputeWholeWigner(double fnorm, int indices[], int ixy, int iq, 
		vector<complex<double>> *aAnm, vector<int> *nindex, vector<int> *mindex, 
		vector<vector<complex<double>>> *ws, vector<double> &data,
		int rank = 0, int mpiprocesses = 1);
	void f_ExportFieldBinary(const char *buffer, 
			vector<double> *xyarr, vector<vector<complex<double>>> *Ea);

	PrintCalculationStatus *m_calcstatus;
	int m_layer;

	Wigner4DManipulator *m_wig4d;
	Spline2D m_fluxspl;
	HermiteGaussianMode *m_hgmode;

	vector<vector<double>> m_xqarr;
	vector<vector<double>> m_data;
	vector<vector<double>> m_XQarr;

	vector<Spline> m_fspl[2];
	double m_r2max;
	double m_rmax;
	vector<vector<double>> m_lgrange[2];
	vector<double> m_flborder;

	vector<vector<complex<double>>> m_Anm;
	vector<vector<complex<double>>> m_anm;
	int m_maxmodenumber;
	double m_cutoff;
	double m_fluxcut;

	FastFourierTransform *m_fft;
	int m_nfftcurr;
	int m_nfftmax;
	double *m_ws;

	double m_lambda;
	int m_mesh[2];
	double m_dxdq[2];
	double m_zwaist;
	double m_srcsize;
	double m_srcdiv;
	double m_norm_factor;
	double m_experr;
	int m_acclevel;

	int m_ncoef;
	int m_mcoef;

	bool m_undersrcopt;
	int m_maxmodecurr;
	Spline m_F0spl;
};

class HGModalDecomp2D
{
public:
	HGModalDecomp2D(PrintCalculationStatus *calcstatus, 
		int acclevel, int maxmodes[], int cmdmode, double cutoff, double fluxcut, Wigner4DManipulator *wig4d);
	~HGModalDecomp2D();
	void LoadData();
	void ComputePrjBeamParameters(double *sigma = nullptr);
	void GetAnmAt(int jxy, int posidx[], vector<vector<complex<double>>> *Anm);
	void GetAnmAll(int jxy, int rank, int mpiprocesses);
	void GetComplexAmp2D(vector<vector<double>> &xyarr,
		vector<vector<vector<complex<double>>>> *Ea, double eps, int pmax,
		int rank = 0, int mpiprocesses = 1, bool skipstep = false);
	void DumpFieldProfile(const char *bufbin, 
		double eps, int pmax, double dxy[], bool iswrite, 
		vector<vector<double>> &xyarr, vector<vector<double>> &datar, vector<vector<double>> &datai,
		int rank, int mpiprocess);
	double GetNormalizeFactor();
	void GetFluxConsistency(int pmax, double eps, vector<double> &fr, vector<double> &fa);
	void ReconstructExport(int pmax, double epsanm, 
		double *CMDerr, vector<vector<vector<double>>> &data, int rank = 0, int mpiprocesses = 1);
	double GetWignerAt(int posxy[], int posxyq[], int nmesh[], int anmesh[]);
	void GetWignerAt(int pmax, double eps,
		double xy[], double dq[], int hqmesh[], vector<double> &W);

	int GetOrderedModeNumber(int seqno);
	double GetExpansionError(){return m_experr;}

	void WriteResults(string &result, double cmderr[]);
	void LoadResults(int maxorder[], double srcsize[], 
		double fnorm, vector<int> &order, vector<double> &anmre, vector<double> &anmim);

	void SetGSModel(bool isGS[], int rank, int processes, double *err);

private:
	void f_ComputeWholeWigner(double fnorm, vector<double> &data, int rank, int mpiprocesses);
	void f_ExportFieldBinary(const char *buffer, 
			vector<vector<double>> *xyarr, vector<vector<vector<complex<double>>>> *Ea);

	Wigner4DManipulator *m_wig4d;
	HGModalDecomp *m_hgmode[3];
	vector<double> m_xyq[NumberWignerUVPrm];
	vector<vector<complex<double>>> m_Anm;
	vector<vector<complex<double>>> m_anm;
	vector<vector<complex<double>>> m_ws[2];
	vector<complex<double>> m_Anm_approx;
	vector<int> m_nindex;
	vector<int> m_mindex;
	vector<int> m_ordered_mode;
	PrintCalculationStatus *m_calcstatus;

	vector<double> m_xyarr[2];
	vector<double> m_qarr[2];
	double m_normfactor;
	int m_nmesh[2];
	int m_anmesh[2];
	double m_lambda;
	double m_srcsize[2];
	int m_maxmode[2];
	double m_cutoff;
	double m_fluxcut;
	int m_max_cmdmode;
	double m_experr;
	int m_acclevel;
};

void GetSparseMatrix(int nmodes,
	vector<vector<complex<double>>> &anmfull, vector<double> anm[], vector<int> anmidx[]);
void WriteCommonJSON(stringstream &ssresult, 
	double cmderr[], int nmodes, double fnorm, vector<double> &anmre, vector<double> &anmim);
void WriteCommonJSON(stringstream &ssresult,
	double cmderr[], double fnorm, vector<double> anm[], vector<int> anmidx[]);
double GetHLGWidth(int n);

double HGFuncDirect(int mode, double xh);
double LGFuncDirect(int n, int m, double r);


#endif
