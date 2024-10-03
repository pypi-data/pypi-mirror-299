#ifndef source_characterization_h
#define source_characterization_h

#include <complex>

#include "spectra_solver.h"
#include "quadrature.h"
#include "optimization.h"
#include "interpolation.h"
#include "fast_fourier_transform.h"
#include "undulator_fxy_far.h"

class FluxDensity;
class Trajectory;
class Particle;

enum {
	WignerFuncType4DX = 0,
	WignerFuncType4DY,
	WignerFuncType2DX,
	WignerFuncType2DY,
	WignerFuncType3DX,
	WignerFuncType3DY,
	WignerFuncTypeXY,

	WignerIntegOrderU = 0,
	WignerIntegOrderV,
	WignerIntegOrderUVcv
};

enum {
	WignerType4D = 0,
	WignerType2DX,
	WignerType2DY,
	NumberWignerTypeForBinary,

	WignerUVPrmU = 0,
	WignerUVPrmV,
	WignerUVPrmu,
	WignerUVPrmv,
	NumberWignerUVPrm,

	Wig4DSolveModeX = 0,
	Wig4DSolveModeY,
	Wig4DSolveSrcAdjX,
	Wig4DSolveSrcAdjY,
	Wig4DRestrPmax,
	Wig4DRestrLowerLimit,
	Wig4DRestrSuffCoeff,
	Wig4DRestrSuffError,
	Wig4DRestrSuffEfield,
	Wig4DRestrSuffEfieldBin,
	Wig4DRestrSuffSWigner,
	Wig4DFprofXDiv,
	Wig4DFprofYDiv,
	NumberWig4DSolvePrms,

	Wig4OReconOptDumpCoef = 0,
	Wig4OReconOptCompareDev,
	Wig4OReconOptEfield,
	Wig4OReconOptEfieldBin,
	Wig4OReconOptWigner,
	Wig4OReconOptComparePlot,
	Wig4OReconOptReuse,
	NumberWig4OReconOpt,

	WigErrorCorrelation = 0,
	WigErrorDeviation,
	WigErrorCoherent,
	NumberWigError,

	Wig4DResSeparable = 0,
	Wig4DResDegCohTotal,
	Wig4DResDegCohX,
	Wig4DResDegCohY,
	NumberWig4DRes,
};


class WignerFunction :
	public QSimpson, FunctionDigitizer
{
public:
	WignerFunction(int acclevel, int nwiggler, bool isund, bool isoddpolewig,
		PrintCalculationStatus *status, int wlayer);
	~WignerFunction();
	bool AssignData(vector<vector<complex<double>>> *Ex, vector<vector<complex<double>>> *Ey,
		int mesh[], double delta[], double eKx = 0, double eKy = 0, 
		double *dinterv = nullptr, double *hrange = nullptr, double epsilon = -1);
	bool AssignDataSn(vector<vector<double> > *Sn, int mesh[], double delta[], double epsilon, int nh, int N);
	bool AssignDataAprof(double aflux, int mesh[], double delta[]);
	void AssignCondition(double sigmauv[], double sigmaUV[], double alpha[]);
	bool SpatialProfileSingleConv(int nc, vector<vector<double> > *we, vector<vector<double> > *wf);
	void SpatialProfileSingle(int nc, 
		vector<vector<double> > *ws, vector<vector<double> > *wa = nullptr, 
		double d_eta = 0, bool isalloc = true, double *duvmin = nullptr);
	void AllocateSpatialProfile(double espread, double *dUVmin = nullptr, double *Umax = nullptr,
			int rank = 0, int mpiprocesses = 1);
	void LoadSpatialProfile(FluxDensity *fluxdens, double espread, double duv[],
		vector<vector<vector<complex<double>>>> *ExFnearp,
		vector<vector<vector<complex<double>>>> *EyFnearp);
	bool AllocateSpatialProfile(int layer, bool iscamp, 
			double gtrange[], double espread, double dqduv, double coefEwxy, 
			FluxDensity *fluxdens, double *dUVmin = nullptr, int rank = 0, int mpiprocesses = 1,
			double *duv = nullptr,
			vector<vector<vector<complex<double>>>> *ExFnearp = nullptr,
			vector<vector<vector<complex<double>>>> *EyFnearp = nullptr);
	void GetWignerPhaseSpaceFnear(int type, 
			double UVfix[], double uvfix[], double uvini[], double uvfin[], int mesh[],
			vector<vector<double> > *W, FluxDensity *fluxdens, int rank, int mpiprocesses, int netgt = -1,
			vector<vector<vector<complex<double>>>> *ExFnearp = nullptr,
			vector<vector<vector<complex<double>>>> *EyFnearp = nullptr);
	void GetWignerPhaseSpace(int type, 
			double UVfix[], double uvfix[], double uvini[], double uvfin[], int mesh[],
			vector<vector<double> > *W, FluxDensity *fluxdens = nullptr, int rank = 0, int mpiprocesses = 1);
	void GetExyAmplitude(double xy[], complex<double> *Ex, complex<double>*Ey);
	double GetFluxSrcPoint(double UV[]);
	double GetSn(double u[], double v[]);
	virtual void QSimpsonIntegrand(int layer, double uv, vector<double> *W);
    virtual double Function4Digitizer(double uv, vector<double> *W);
	void GetSrcProfile(double dqduv, double coefExy, double uvrange[], double UVini[], double UVfin[], int mesh[], 
			double espread, vector<vector<double> > *W, FluxDensity *fluxdens = nullptr, int rank = 0, int mpiprocesses = 1);
	void SetIrpt(bool ison);
	void SetEwxyPointer(int eindex);
	int GetProcessLayer(){return m_process_layer;}

private:
	void f_AllocateEwxyAxis(
		int ndatapoints, int nc, vector<double> *values,	bool isodd, int halfmesh, double dtheta, 
		int jxy, vector<complex<double> > *Ewx, vector<complex<double> > *Ewy, FluxDensity *fluxdens);
	bool f_IsEvaluateGtEiwt(bool isx, double range[], double w);
	double f_GetOmegaWiggler(int index, double delta = 0.0);
	void f_ReIntegrateEwit(int nc, int np, double w, int N, 
		vector<double> *arg, vector<vector<double> > *values, vector<double> *W);
	void f_GetWignerAlongUV(
		double uvfix, vector<double> *UVarr, vector<vector<double> > *W,
		int rank = 0, int mpiprocesses = 1);
	void f_Integrand_u(double u, vector<double> *W);
	void f_Integrand_v(double v, vector<double> *W);
	void f_Convolute_uv(int uvidx, double uv, vector<double> *W);
	void f_GetIntegRangeCV(int uvidx, double uvrange[]);
	void f_GetFTRange(int uvidx, double uvrange[]);
	void f_PutZeroValues(vector<double> *W, int np = 1);
	int f_GetSkipNumber(double *data, int nfft, bool isamp);
	void f_GetIntegralLevel(double range[], int uvidx, int level[]);
	void f_AssignSpRange();
	void f_ConfigMesh();
	void f_ClearPointers();

	void f_ApplyBMSourceFlux(double U);

	vector<vector<double> > *m_Sn;
	vector<vector<complex<double>>> *m_Exp;
	vector<vector<complex<double>>> *m_Eyp;
	vector<double> m_wsarg[WignerIntegOrderUVcv+1];
	vector<vector<double> > m_wsval[WignerIntegOrderUVcv+1];
	vector<double> m_UVpoints;
	vector<double> m_wsorg;
	vector<double> m_psiseg;

	vector<vector<vector<double>>> m_e;
	vector<vector<vector<double>>> m_f;

	int m_nfft[2];
	int m_nskip[2];
	FastFourierTransform *m_fft[2];
	double *m_wsdata[2];
	double *m_wadata[2];

	Spline m_bmsrcfspl[2];
	vector<double> m_Varr4bm;
	vector<double> m_Earr4bm[2];
	double *m_ws4bm;
	FastFourierTransform *m_fft4bm;
	double m_epsbm;
	bool m_idealbm;
	int m_nfftbm;

	vector<vector<vector<complex<double>>>> m_ExFnear;
	vector<vector<vector<complex<double>>>> m_EyFnear;
	vector<double> m_earray;
	int m_nepoints;
	int m_neindex;

	// grid condition for ideal sources
	int m_halfmesh[2];
	double m_delta[2];
	int m_mesh[2];
	double m_valrange[2];
	double m_dinterv[2];
	double m_halfrange[2];

	// grid condition for E-convoluted sinc func. for undulators
	double m_Uepsilon;
	int m_Nnh;
	int m_halfmeshsn[2];
	double m_deltasn[2];
	int m_snmesh[2];
	double m_valrangesn[2];

	// grid condition for aungular profiles for wigglers
	double m_sflux;
	double m_aflux;
	double m_adelta[2];
	int m_amesh[2];
	int m_speini[2];
	int m_spefin[2];

	// grid condition for spatial profiles
	vector<double> m_deltasp[2];
	vector<int> m_spmesh[2];
	vector<int> m_halfmeshsp[2];
	vector<double> m_valrangesp[2];

	// source conditions etc.
	double m_gaussian_limit;
	double m_eKwiggler;
	double m_eKx;
	int m_acclevel;
	int m_type;
	int m_irpt;
	bool m_isnegpole;
	bool m_isund;
	bool m_oddpolewig;
	int m_Nwiggler;
	int m_ncomps;
	double m_srcpoint[2];
	int m_nUVpoints;

	// e-beam conditions
	double m_sigmauv[2];
	double m_sigmaUV[2];
	double m_alpha[2];

	// convolution variables
	int m_uvcvidx;
	int m_uvscidx;
	double m_uvfix[2];
	double m_uvvar[2];
	double m_uvcv[2];

	// •Û—¯
	double m_espreadloc;

	PrintCalculationStatus *m_calcstatus;
	int m_process_layer;

	//----->>>>>
	int m_rep;
};

class SourceCharacterization :
    public SpectraSolver
{
public:
    SourceCharacterization(double ephoton, SpectraSolver &spsolver, int wlayer, bool zerodiv = false);

	~SourceCharacterization();
	void GetPhaseSpaceProfile(int type, double fixpoint[], 
		double rangeini[], double rangefin[], int meshr[],
			vector<vector<double> > *xyarray, vector<vector<double> > *W, 
			FluxDensity *fluxdens = nullptr, int rank = 0, int mpiprocesses = 1, bool skipalloc = false,
			double *duv = nullptr, int netgt = -1,
			vector<vector<vector<complex<double>>>> *ExFnearp = nullptr,
			vector<vector<vector<complex<double>>>> *EyFnearp = nullptr);
	void GetSourceSize(double angle[], double size[], int rank = 0 , int mpiprocesses = 1);
	void GetSrcProfile(double XYini[], double XYfin[], int mesh[], 
		vector<vector<double> > *xyarray, vector<vector<double> > *W, FluxDensity *fluxdens = nullptr, int rank = 0, int mpiprocesses = 1);
	double GetCoefSpatialProfile();
	double GetWavelength(){return m_wavelength;}

private:
	vector<vector<complex<double>>> m_Ex;
	vector<vector<complex<double>>> m_Ey;
	vector<vector<double>> m_Sn;

	double f_GTmaxU(double epsilon, int nh, int N, double *gt2uv, double *hDelta);
	void f_AssignEFieldUnd(double epsilon, int nh, int N);
	void f_AssignSn(double uvmax, double epsilon, int nh, int N);
	void f_AssignEFieldWiggler(double epsilon, double deltau, bool isbma);
	void f_AssignEFieldBM(double epsilon, double deltau);
	void f_GetBMExyAmpDirect(double epsilon, double uv[], complex<double> *Ex, complex<double> *Ey);
	WignerFunction *m_wigner;
	double m_dqduv;
	double m_dXYdUV;
	double m_coefExy;
	double m_wavelength;
	double m_coefWDF;
	double m_esigma;
	bool m_isidealund;
	bool m_issinglebm;
	double m_penergy;
	double m_ecritical;
	double m_sigmaxy[2];
	double m_dUmin;
	double m_gtrange[2];
};

#endif
