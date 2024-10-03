#include <boost/math/special_functions/laguerre.hpp>
#include <boost/math/special_functions/hermite.hpp>
#include <Eigen/Dense>
#include <Eigen/Eigenvalues> 

#include "numerical_common_definitions.h"
#include "optimization.h"
#include "interpolation.h"
#include "quadrature.h"
#include "hermite_gauss_decomp.h"
#include "output_utility.h"
#include "json_writer.h"

#ifdef __NOMPI__
#include "mpi_dummy.h"
#else
#include "mpi.h"
#endif

using namespace boost::math;
using namespace std;
using namespace Eigen;

void WriteCommonJSON(stringstream &ssresult, 
	double cmderr[], int nmodes, double fnorm, vector<double> &anmre, vector<double> &anmim)
{
	PrependIndent(JSONIndent, ssresult);
	ssresult << fixed << setprecision(1);
	ssresult << "\"" << CMDErrorLabel << "\"" << 
		": {\"" << MatrixErrLabel << "\": \"" << cmderr[0]*100 << "%\"" 
		<< ", \"Flux Consistency\": \"" << cmderr[1]*100 << "%\"";
	if(cmderr[2] >= 0){
		ssresult << ", \"Wigner Function Consistency\": \"" << (1.0-cmderr[2])*100 << "%\"";
	}
	ssresult << "}," << endl;
	ssresult << defaultfloat << setprecision(6);

	WriteJSONValue(ssresult, JSONIndent, fnorm, NormFactorLabel.c_str(), false, true);

	PrependIndent(JSONIndent, ssresult);
	ssresult << "\"" << AmplitudeReLabel << "\"" << ": [" << endl;
	PrependIndent(2*JSONIndent, ssresult);
	WriteJSONData(ssresult, 2*JSONIndent, anmre, nmodes, false, false);
	ssresult << endl;
	PrependIndent(JSONIndent, ssresult);
	ssresult << "]," << endl;

	PrependIndent(JSONIndent, ssresult);
	ssresult << "\"" << AmplitudeImLabel << "\"" << ": [" << endl;
	PrependIndent(2*JSONIndent, ssresult);
	WriteJSONData(ssresult, 2*JSONIndent, anmim, nmodes, false, false);
	ssresult << endl;
	PrependIndent(JSONIndent, ssresult);
	ssresult << "]" << endl << "}";
}

//-----------
HermiteGaussianMode::HermiteGaussianMode(double sigma, double lambda, int maxorder)
{
	m_sigma = sigma;
	m_lambda = lambda;
	m_maxorder = maxorder;
	m_hgcoef.resize(maxorder+1, 0.0);
	m_lgcoef.resize(maxorder+1);
	for(int m = 0; m <= maxorder; m++){
		m_lgcoef[m].resize(maxorder+1, 0.0);
	}
}

double HermiteGaussianMode::GetField(int mode, double x)
{
	double xh = x/2.0/SQRTPI/m_sigma;
	return HGFunc(mode, xh);
}

void HermiteGaussianMode::GetWigner(int n, int m, double x, double theta, double *W)
{
	double sigpi = 2.0*SQRTPI*m_sigma;
	double xh = x/sigpi;
	double qh = theta/m_lambda*sigpi;
	double r = sqrt(hypotsq(xh, qh));
	double phi = 0;
	if(r > 0){
		phi = (double)(m-n)*atan2(qh, xh);
	}
	double lg = LGFunc(n, m, r)*2.0*sqrt(PI)*m_sigma;
	W[0] = lg*cos(phi);
	W[1] = lg*sin(phi);
}

double HermiteGaussianMode::HGFunc(int mode, double xh)
{
	if(mode > m_maxorder){
		return 0.0;
	}

	if(m_hgcoef[mode] < INFINITESIMAL){
		m_hgcoef[mode] = 1.0/SQRT2;
		for(int m = 1; m <= mode; m++){
			m_hgcoef[mode] *= (double)(2*m);
		}
		m_hgcoef[mode] = 1.0/sqrt(m_hgcoef[mode]);
	}

	double tex = xh*xh*PI;
	if(tex > MAXIMUM_EXPONENT){
		return 0.0;
	}

	return m_hgcoef[mode]*exp(-tex)*hermite(mode, SQRTPI2*xh);
}

double HermiteGaussianMode::LGFunc(int n, int m, double r)
{
	if(n > m_maxorder || m > m_maxorder){
		return 0.0;
	}

	int l = min(n, m);
	int k = abs(n-m);

	if(m_lgcoef[n][m] < INFINITESIMAL){
		double frac = 1.0;
		for(int i = l+1; i <= l+k; i++){
			frac *= (double)i;
		}
		m_lgcoef[n][m] = 2.0*pow(2.0*PI2, 0.5*(double)k)/sqrt(frac)*(l%2 > 0 ? -1.0 : 1.0);
		m_lgcoef[m][n] = m_lgcoef[n][m];
	}

	double tex = r*r*PI2;
	if(tex > MAXIMUM_EXPONENT){
		return 0.0;
	}
	double lg = m_lgcoef[n][m]*exp(-tex)*laguerre(l, k, 2.0*tex);
	if(k > 0){
		lg *= pow(fabs(r), k);
	}
	return lg;
}

//---------------------------
// files for debugging
string IntegCMDAlongCF;
string IntegCMDAlongR;
string CMDAmn1D;
string CMDCholeskyBef;
string CMDCholeskyAft;
string CMDFourierTheta;
string CMDFourierPhiBef;
string CMDFourierPhiAft;
string CMD_Anm_Func_1st;
string CMD_Anm_Func_2nd;

HGModalDecomp::HGModalDecomp(int layer,
	PrintCalculationStatus *calcstatus, int kmax, double cutoff, Wigner4DManipulator *wig4d)
{
#ifdef _DEBUG
//IntegCMDAlongCF = "..\\debug\\CMD_integ_along_cf.dat";
//IntegCMDAlongR = "..\\debug\\CMD_integ_along_r.dat";
//CMDAmn1D = "..\\debug\\CMD_Amn_1d.dat";
//CMDCholeskyBef = "..\\debug\\CMD_Cholesky_bef.dat";
//CMDCholeskyAft = "..\\debug\\CMD_Cholesky_aft.dat";
//CMDFourierTheta = "..\\debug\\CMD_FFT_theta.dat";
//CMDFourierPhiBef = "..\\debug\\CMD_FFT_phi_bef.dat";
//CMDFourierPhiAft = "..\\debug\\CMD_FFT_phi_aft.dat";
//CMD_Anm_Func_1st= "..\\debug\\CMD_Anm_1st.dat";
//CMD_Anm_Func_2nd= "..\\debug\\CMD_Anm_2nd.dat";
#endif

	m_calcstatus = calcstatus;
	m_layer = layer;
	m_lambda = wig4d->GetWavelength();
	m_fft = nullptr;
	m_nfftcurr = m_nfftmax = 0;
	m_ws = nullptr;
	m_hgmode = nullptr;
	m_maxmodenumber = kmax;
	m_cutoff = cutoff;
	m_undersrcopt = false;
	m_wig4d = wig4d;
	AllocateMemorySimpson(2, 2, 1);
}

HGModalDecomp::~HGModalDecomp()
{
	if(m_fft != nullptr){
		delete m_fft;
	}
	if(m_ws != nullptr){
		free(m_ws);
	}
	if(m_hgmode != nullptr){
		delete m_hgmode;
	}
}

void HGModalDecomp::LoadData()
{
	int type = m_wig4d->GetType();
	int jxy, idr[2], indices[NumberWignerUVPrm];
	if(type == WignerType2DX){
		jxy = 0;
		idr[0] = WignerUVPrmU;
		idr[1] = WignerUVPrmu;
		indices[WignerUVPrmV] = indices[WignerUVPrmv] = 0;
	}
	else{
		jxy = 1;
		idr[0] = WignerUVPrmV;
		idr[1] = WignerUVPrmv;
		indices[WignerUVPrmU] = indices[WignerUVPrmu] = 0;
	}
	m_xqarr.resize(2);
	m_wig4d->GetXYQArray(jxy, m_xqarr[0], m_xqarr[1]);

	for(int j = 0; j < 2; j++){
		m_xqarr[j] *= 1.0e-3; // mm -> m, mrad -> rad
		m_XQarr.push_back(m_xqarr[j]);
		m_mesh[j] = (int)m_xqarr[j].size();
		m_dxdq[j] = m_xqarr[j][1]-m_xqarr[j][0];
	}

	m_data.resize(m_mesh[0]);
	for(int n = 0; n < m_mesh[0]; n++){
		m_data[n].resize(m_mesh[1]);
		indices[idr[0]] = n;
		for(int m = 0; m < m_mesh[1]; m++){
			indices[idr[1]] = m;
			m_data[n][m] = m_wig4d->GetValue(indices);
		}
	}
	SetBeamParameters();
}

bool HGModalDecomp::AssingData(vector<vector<double>> *xyqarr, 
	vector<vector<double>> &data, bool isstat)
{
	m_data = data;
	if(xyqarr != nullptr){
		m_xqarr = *xyqarr;
		for(int j = 0; j < 2; j++){
			m_xqarr[j] *= 1.0e-3; // mm,mrad -> m,rad
			m_mesh[j] = (int)m_xqarr[j].size();
			m_dxdq[j] = m_xqarr[j][1]-m_xqarr[j][0];
		}
	}
	if(isstat){
		SetBeamParameters();
	}
	else{
		m_fluxspl.SetSpline2D(m_mesh, &m_xqarr[0], &m_xqarr[1], &m_data, false);
	}
	return true;
}

void HGModalDecomp::SetBeamParameters()
{
	double sigma[2], alpha, beta, emitt;
	vector<string> titles(3);
	titles[0] = TitleLablesDetailed[SrcX_];
	titles[1] = TitleLablesDetailed[SrcQX_];
	titles[2] = TitleLablesDetailed[Brill1D_];
	DataContainer datacont;
	vector<vector<vector<double>>> values(1);
	values[0] = m_data;
	datacont.Set2D(titles, m_xqarr, values);
	datacont.GetStatistics(sigma, &emitt, &alpha, 0);
	beta = sigma[0]*sigma[0]/emitt;
	m_zwaist = beta*alpha/hypotsq(alpha, 1.0);
	m_srcsize = sigma[0]/sqrt(hypotsq(alpha, 1.0));
}

void HGModalDecomp::SetAnm(vector<vector<complex<double>>> *Anm)
{
	m_Anm.resize(m_maxmodenumber+1);
	for(int n = 0; n <= m_maxmodenumber; n++){
		m_Anm[n].resize(m_maxmodenumber+1);
		for(int m = 0; m <= m_maxmodenumber; m++){
			m_Anm[n][m] = (*Anm)[n][m];
		}
	}
}

void HGModalDecomp::CreateHGMode(double *norm)
{
	if(norm != nullptr){
		m_hgmode = new HermiteGaussianMode(m_srcsize*(*norm), m_lambda, m_maxmodenumber);
	}
	else{
		m_hgmode = new HermiteGaussianMode(m_srcsize, m_lambda, m_maxmodenumber);
	}
}

int HGModalDecomp::GetIntegrateRange(vector<vector<double>> &r2range, bool forcedebug)
{
	int l = min(m_ncoef, m_mcoef);

	// fitting parameters
	double coef = 0.23; 
	double exponent = 0.65;
	double offset = 1.9;
	// envelope width of Gauss-Laguerre function
	double width = coef*pow(l, exponent)+offset;
	double bwidth = 0.01*width;

	if(m_lgrange[0][m_ncoef][m_mcoef] < 0){
		double eps = 1.0e-6; // cut off of LGFunc
		double dr = 0.1; // increment to search the start position of integration
		double rini = 0;
		double lgg;
		lgg = fabs(m_hgmode->LGFunc(m_ncoef, m_mcoef, rini+dr));
		while(lgg < eps) {
			rini += dr;
			lgg = fabs(m_hgmode->LGFunc(m_ncoef, m_mcoef, rini+dr));
		}
		if(rini < bwidth){ // 0~rini is not so wide compared to the envelope width
			m_lgrange[0][m_ncoef][m_mcoef] = 0;
		}
		else{
			m_lgrange[0][m_ncoef][m_mcoef] = rini;
		}
		if(rini > m_rmax){
			m_lgrange[0][m_ncoef][m_mcoef] = 0;
			m_lgrange[1][m_ncoef][m_mcoef] = rini;
		}
		else{
			double rfin = rini+width;
			if(m_rmax-rfin < bwidth){// rfin~m_rmax is not so wide, or rfin > m_rmax
				m_lgrange[1][m_ncoef][m_mcoef] = m_rmax;
			}
			else{
				m_lgrange[1][m_ncoef][m_mcoef] = rfin;
			}
		}
	}

	int k = abs(m_ncoef-m_mcoef);
	double flborder = m_flborder[k]; // 0~flborder: large flux range
	double dw = width/(1.0+l)*4.0; // width for 4 peaks
	int nbins[2] = {0, 0}, nsec = 1;
	double border[3], wbins[2];

	border[0] = m_lgrange[0][m_ncoef][m_mcoef];
	if(flborder > m_lgrange[0][m_ncoef][m_mcoef]+bwidth 
		&& flborder < m_lgrange[1][m_ncoef][m_mcoef]-bwidth){
		nsec = 2;
		border[1] = flborder;
	}
	border[nsec] = m_lgrange[1][m_ncoef][m_mcoef];

	int ndiv = 0;
	for(int j = 0; j < nsec; j++){
		wbins[j] = border[j+1]-border[j];
		nbins[j] = max(1, (int)floor(0.5+wbins[j]/dw));
		wbins[j] /= nbins[j];
		ndiv += nbins[j];
	}

	if(r2range.size() < 2){
		r2range.resize(2);
	}
	if(r2range[0].size() < ndiv+2){
		for(int j = 0; j < 2; j++){
			r2range[j].resize(ndiv+2);
		}
	}

	int ndivtot = ndiv, ntr = 0;
	for(int j = 0; j < nsec; j++){
		for (int n = 0; n < nbins[j]; n++){
			r2range[0][ntr] = border[j]+n*wbins[j];
			r2range[1][ntr] = r2range[0][ntr]+wbins[j];
			ntr++;
		}
	}

	if(m_lgrange[1][m_ncoef][m_mcoef] < m_rmax){
		ndivtot++;
		r2range[0][ndiv] = r2range[1][ndiv-1];
		r2range[1][ndiv] = m_rmax;
	}
	if(m_lgrange[0][m_ncoef][m_mcoef] > 0){
		ndivtot++;
		r2range[0][ndivtot-1] = 0;
		r2range[1][ndivtot-1] = r2range[0][0];
	}
	for(int n = 0; n < ndivtot; n++){
		for(int j = 0; j < 2; j++){
			r2range[j][n] *= r2range[j][n];
		}
	}
	return ndivtot;
}

void HGModalDecomp::GetAnm(vector<vector<complex<double>>> *Anm, 
	int rank, int mpiprocesses, bool forcedebug)
{
	double eps = 0.01;
	int layers[2] = {0, -1};
	vector<double> result(2), rsum(2);
	vector<vector<double>> finit(1);
	finit[0].resize(2, 0.0);

	if(m_hgmode != nullptr){
		delete m_hgmode;
	}
	CreateHGMode();
	m_Anm.resize(m_maxmodenumber+1);

	m_calcstatus->SetSubstepNumber(m_layer, (m_maxmodenumber+1)/mpiprocesses);

	vector<vector<double>> r2range;
	int repmin[] = {7, 5}, idrep;

	for(int n = 0; n <= m_maxmodenumber; n++){
		m_ncoef = n;
		m_Anm[n].resize(m_maxmodenumber+1);
		if(rank != (n%mpiprocesses)){
			continue;
		}
		for(int m = 0; m <= n; m++){
			finit[0][0] = finit[0][1] = 0;
			m_mcoef = m;

#ifndef OLDSCHEME
			int ndiv = GetIntegrateRange(r2range, forcedebug);
			IntegrateSimpson(layers, r2range[0][0], r2range[1][0], eps, repmin[0], &finit, &rsum, IntegCMDAlongR);
			for(int nrr = 1; nrr < ndiv; nrr++){
				idrep = nrr < ndiv-2 ? 0 : 1;
				IntegrateSimpson(layers, r2range[0][nrr], r2range[1][nrr], eps, repmin[idrep], &finit, &result, IntegCMDAlongR, true);
				rsum += result;
			}
#else		
			int nreg = (int)ceil(m_r2max);
			double dreg = m_r2max/nreg;
			int jrepmin = 5;
			int morder = min(m_ncoef, m_mcoef);
			while(morder > 1){
				morder >>= 1;
				jrepmin++;
			}

			IntegrateSimpson(layers, 0, dreg, eps, jrepmin, &finit, &rsum, IntegCMDAlongR);
			for(int nrr = 1; nrr < nreg; nrr++){
				IntegrateSimpson(layers, nrr*dreg, (nrr+1)*dreg, 
					eps, jrepmin, &finit, &result, IntegCMDAlongR, true);
				rsum += result;
			}
#endif
			m_Anm[n][m] = complex<double>(rsum[0], rsum[1]);
		}
		m_calcstatus->AdvanceStep(m_layer);
	}

	if(mpiprocesses > 1){
		double *ws = new double[2*(m_maxmodenumber+1)];
		for (int n = 0; n <= m_maxmodenumber; n++){
			int currrank = n%mpiprocesses;
			if(rank == currrank){
				for (int m = 0; m <= n; m++){
					ws[2*m] = m_Anm[n][m].real();
					ws[2*m+1] = m_Anm[n][m].imag();
				}
			}
			MPI_Bcast(ws, 2*(n+1), MPI_DOUBLE, currrank, MPI_COMM_WORLD);
			if(rank != currrank){
				for (int m = 0; m <= n; m++){
					m_Anm[n][m] = complex<double>(ws[2*m], ws[2*m+1]);
				}
			}
		}
		delete[] ws;
	}

	for(int n = 0; n <= m_maxmodenumber; n++){
		for(int m = 0; m < n; m++){
			m_Anm[m][n] = conj(m_Anm[n][m]);
		}
	}

	if(Anm != nullptr){
		if(Anm->size() < m_maxmodenumber+1){
			Anm->resize(m_maxmodenumber+1);
		}
		for(int n = 0; n <= m_maxmodenumber; n++){
			if((*Anm)[n].size() < m_maxmodenumber+1){
				(*Anm)[n].resize(m_maxmodenumber+1);
			}
			for(int m = 0; m <= m_maxmodenumber; m++){
				(*Anm)[n][m] = m_Anm[n][m];
			}
		}
	}

#ifdef _DEBUG
	if(!CMDAmn1D.empty()){
		ofstream debug_out(CMDAmn1D);
		vector<double> values(2*(m_maxmodenumber+2));
		for (int n = 0; n <= m_maxmodenumber; n++){
			values[0] = n;
			for (int m = 0; m <= m_maxmodenumber; m++){
				values[1] = m;
				values[2*m+2] = m_Anm[m][n].real();
				values[2*m+3] = m_Anm[m][n].imag();
				PrintDebugItems(debug_out, values);
			}
		}
	}
#endif
}

double HGModalDecomp::CostFunc(double x, vector<double> *y)
{
	double eps = 0.01;
	int layers[2] = {0, -1};
	double xqrange[2];
	for(int j = 0; j < 2; j++){
		xqrange[j] = minmax(m_xqarr[j], true);
	}
	double r2lim = max(xqrange[0]/x, xqrange[1]*x);
	double dhr = min(m_dxdq[0]/x, m_dxdq[1]*x);
	int rmesh = (int)floor(sqrt(hypotsq(xqrange[0]/x, xqrange[1]*x))/dhr);

	vector<double> rarr(rmesh+1), farr(rmesh+1);
	for(int nr = 0; nr <= rmesh; nr++){
		rarr[nr] = dhr*(double)nr;
		int nphi = max(16, (int)ceil(PI2*rarr[nr]/dhr));
		double dphi = PI2/nphi, phi, xq[3], flux;
		farr[nr] = 0;
		for(int n = 0; n < nphi; n++){
			phi = (n+0.5)*dphi;
			xq[0] = rarr[nr]*cos(phi)*x;
			if(fabs(xq[0]) > xqrange[0]){
				continue;
			}
			xq[1] = rarr[nr]*sin(phi)/x;
			if(fabs(xq[1]) > xqrange[1]){
				continue;
			}
			flux = m_fluxspl.GetValue(xq, true);
			farr[nr] += flux*dphi;
		}
	}
	m_F0spl.SetSpline(rmesh+1, &rarr, &farr, true);

	double fmax = minmax(farr, true);
	m_flborder[0] = rarr[rmesh];
	for(int nr = rmesh; nr >= 0; nr--){
		if(farr[nr] >= 0.1*fmax){
			m_flborder[0] = rarr[nr];
			break;
		}
	}

	m_rmax = r2lim;
	r2lim *= r2lim;

	vector<double> result(2, 0.0), rsum(2, 0.0);
	vector<vector<double>> finit(1);
	finit[0].resize(2);

	if(m_hgmode != nullptr){
		delete m_hgmode;
	}
	CreateHGMode(&x);
	m_normsrcsize = x;

	double Asum = 0;
	int repmin[] = {7, 5}, idrep;
	vector<vector<double>> r2range;

	m_maxmodecurr = m_maxmodenumber;
	for(int mn = 0; mn <= m_maxmodenumber; mn++){
		m_mcoef = m_ncoef = mn;

#define OLDSCHEME
#ifndef OLDSCHEME
			int ndiv = GetIntegrateRange(r2range, false);
			IntegrateSimpson(layers, r2range[0][0], r2range[1][0], eps, repmin[0], &finit, &rsum, IntegCMDAlongCF);
			for(int nrr = 1; nrr < ndiv; nrr++){
				idrep = nrr < ndiv-2 ? 0 : 1;
				IntegrateSimpson(layers, r2range[0][nrr], r2range[1][nrr], eps, repmin[idrep], &finit, &result, IntegCMDAlongCF, true);
				rsum += result;
			}
#else
		int nreg = (int)ceil(r2lim);
		double dreg = r2lim/nreg;
		finit[0][0] = finit[0][1] = 0;
		int jrepmin = 5;
		int morder = min(m_ncoef, m_mcoef);
		while(morder > 1){
			morder >>= 1;
			jrepmin++;
		}
		IntegrateSimpson(layers, 0, dreg, eps, jrepmin, &finit, &rsum, IntegCMDAlongCF);
		for(int nrr = 1; nrr < nreg; nrr++){
			IntegrateSimpson(layers, nrr*dreg, (nrr+1)*dreg, 
				eps, jrepmin, &finit, &result, IntegCMDAlongCF, true);
			rsum += result;
		}
#endif
#undef OLDSCHEME

		Asum += rsum[0];
		if(rsum[0]/Asum < 0.001){
			m_maxmodecurr = mn;
			break;
		}
	}

	for(int mn = 0; mn <= m_maxmodenumber; mn++){
		// reset m_lgrange (Gauss-Laguerre range) because m_rmax changes
		for(int j = 0; j < 2; j++){
			m_lgrange[j][mn][mn] = -1;
		}
	}

	return 1.0-Asum;
}

void HGModalDecomp::QSimpsonIntegrand(int layer, double r2, vector<double> *density)
{
	double rh = sqrt(r2);
	double WLG = m_hgmode->LGFunc(m_ncoef, m_mcoef, rh)/m_norm_factor;

	if(m_undersrcopt){
		(*density)[0] = 0.5*WLG*m_F0spl.GetValue(rh);
		(*density)[1] = 0;
	}
	else{
		int kmn = abs(m_ncoef-m_mcoef);
		(*density)[0] = 0.5*WLG*m_fspl[0][kmn].GetValue(rh, true);
		(*density)[1] = 0.5*WLG*m_fspl[1][kmn].GetValue(rh, true);
	}
}

complex<double> HGModalDecomp::GetComplexAmpSingle(int mode, double eps, double xh)
{
	complex<double> Es(0.0, 0.0);
	for(int m = 0; m <= m_maxmodenumber; m++){
		if(abs(m_anm[m][mode]) > eps){
			double hgf = m_hgmode->HGFunc(m, xh);
			Es += hgf*m_anm[m][mode];
		}
	}
	return Es;
}

void HGModalDecomp::GetComplexAmp(vector<double> &xyarr, 
	vector<vector<complex<double>>> *Ea, double eps, int pmax, bool issimple,
	vector<vector<complex<double>>> *anmarr, vector<vector<int>> *modearr)
{
	double sigpi = 2.0*SQRTPI*m_srcsize;
	int mesh = (int)xyarr.size();

	if(anmarr != nullptr){
		pmax = (int)anmarr->size()-1;
	}
	else{
		pmax = GetMaxOrder(pmax);
	}

	if(Ea->size() < pmax+1){
		Ea->resize(pmax+1);
	}

	m_calcstatus->SetSubstepNumber(m_layer, pmax+1);
	for(int mode = 0; mode <= pmax; mode++){
		if((*Ea)[mode].size() < mesh){
			(*Ea)[mode].resize(mesh);
		}
		for(int nx = 0; nx < mesh; nx++){
			if(anmarr != nullptr){
				(*Ea)[mode][nx] = complex<double>(0.0, 0.0);
				for(int k = 0; k < (*anmarr)[mode].size(); k++){
					double hgf = m_hgmode->HGFunc((*modearr)[mode][k], xyarr[nx]/sigpi);
					(*Ea)[mode][nx] += hgf*(*anmarr)[mode][k];
				}
			}
			else if(issimple){
				(*Ea)[mode][nx] = m_hgmode->HGFunc(mode, xyarr[nx]/sigpi);
			}
			else{
				(*Ea)[mode][nx] = GetComplexAmpSingle(mode, eps, xyarr[nx]/sigpi);
			}
		}
		m_calcstatus->AdvanceStep(m_layer);
	}
}

void HGModalDecomp::GetApproximatedAnm(int pmax, double eps, 
		vector<complex<double>> *aAnm, vector<int> *nindex, vector<int> *mindex)
{
	pmax = GetMaxOrder(pmax);
	aAnm->clear(); nindex->clear(); mindex->clear();
	complex<double> Anm;

	for(int n = 0; n <= m_maxmodenumber; n++){
		for(int m = 0; m <= m_maxmodenumber; m++){
			Anm = complex<double>(0.0, 0.0);
			for(int p = 0; p <= pmax; p++){
				if(abs(m_anm[n][p]) > eps && abs(m_anm[m][p]) > eps){
					Anm = Anm+m_anm[n][p]*conj(m_anm[m][p]);
				}
			}
			if(abs(Anm) > eps*eps){
				aAnm->push_back(Anm);
				nindex->push_back(n);
				mindex->push_back(m);
			}
		}
	}
}

void HGModalDecomp::GetFluxConsistency(int pmax, double eps, vector<double> &fa)
{
	pmax = GetMaxOrder(pmax);

	fa.resize(1+pmax, 0.0);
	for(int p = 0; p <= pmax; p++){
		if(p == 0){
			fa[p] = 0;
		}
		else{
			fa[p] = fa[p-1];
		}
		for(int n = p; n <= m_maxmodenumber; n++){
			double ff = abs(m_anm[n][p]);
			if (ff > eps){
				fa[p] += ff*ff;
			}
		}
	}
}

void HGModalDecomp::ReconstructExport(
	int pmax, double epsanm, double *CMDerr, vector<double> &data, int rank, int mpiprocesses)
{
	vector<double> stderror[NumberWigError];
	double errors[NumberWigError];
	vector<complex<double>> aAnm;
	vector<int> mindex, nindex;
	vector<vector<complex<double>>> ws;
	complex<double> Wrrc;
	int indices[NumberWignerUVPrm], iq, ixy, mesh[2];
	double fnorm;

	pmax = GetMaxOrder(pmax);
	fnorm = m_norm_factor/(2.0*SQRTPI*m_srcsize);

	for(int j = 0; j < 2; j++){
		mesh[j] = (int)m_XQarr[j].size();
	}
	data.resize(mesh[0]*mesh[1]);

	f_AssignWignerArray(&ws, &m_XQarr[0], &m_XQarr[1]);

	if(m_wig4d->GetType() == WignerType2DX){
		indices[WignerUVPrmV] = 0;
		indices[WignerUVPrmv] = 0;
		ixy = WignerUVPrmU;
		iq = WignerUVPrmu;
	}
	else{
		indices[WignerUVPrmU] = 0;
		indices[WignerUVPrmu] = 0;
		ixy = WignerUVPrmV;
		iq = WignerUVPrmv;
	}

	double degcoh;
	GetApproximatedAnm(pmax, epsanm, &aAnm, &nindex, &mindex);
	f_ComputeWholeWigner(
		fnorm, indices, ixy, iq, &aAnm, &nindex, &mindex, &ws, data, rank, mpiprocesses);
	m_wig4d->GetCoherenceDeviation(&degcoh, errors, data);
	*CMDerr = errors[WigErrorDeviation];
}

int HGModalDecomp::GetMaxOrder(int pmax)
{
	if(pmax < 0){
		pmax = m_maxmodenumber;
	}
	else{
		pmax = min(m_maxmodenumber, pmax);
	}
	return pmax;
}

double HGModalDecomp::CholeskyDecomp(vector<vector<complex<double>>> *anm, vector<int> *order)
{
	vector<double> AA(m_maxmodenumber+1);
	vector<int> index(m_maxmodenumber+1);
	for(int n = 0; n <= m_maxmodenumber; n++){
		AA[n] = m_Anm[n][n].real();
		index[n] = n;
	}
	sort(AA, index, m_maxmodenumber+1, false);
	if(order != nullptr){
		order->resize(m_maxmodenumber+1);
		for(int n = 0; n <= m_maxmodenumber; n++){
			(*order)[n] = index[n];
		}
	}

	MatrixXcd A = MatrixXcd::Zero(m_maxmodenumber+1, m_maxmodenumber+1);
	
	double Asum = 0;
	for(int n = 0; n <= m_maxmodenumber; n++){
		for(int m = 0; m <= m_maxmodenumber; m++){
			A(n, m) = m_Anm[index[n]][index[m]];
		}
		Asum += A(n, n).real();
	}

	SelfAdjointEigenSolver<MatrixXcd> ES(A);
	vector<double> eig(m_maxmodenumber+1);
	bool ispos = true;
	for(int i = 0; i <= m_maxmodenumber; i++){
		eig[i] = ES.eigenvalues()(i);
		if(eig[i] < 0){
			ispos = false;
			break;
		}
	}

	if(!ispos){
		MatrixXcd V = ES.eigenvectors();
		MatrixXcd Vinv = V.inverse();
		MatrixXcd D = MatrixXcd::Zero(m_maxmodenumber+1, m_maxmodenumber+1);
		for(int i = 0; i <= m_maxmodenumber; i++){
			D(i, i) = max(0.0, ES.eigenvalues()(i));
		}
		
#ifdef _DEBUG
		if (!CMDCholeskyBef.empty()){
			ofstream debug_out(CMDCholeskyBef);
			vector<double> values(m_maxmodenumber+2);
			for(int n = 0; n <= m_maxmodenumber; n++){
				values[0] = eig[n];
				for(int m = 0; m <= m_maxmodenumber; m++){
					values[m+1] = A(n, m).real();
				}
				PrintDebugItems(debug_out, values);
			}
		}
#endif

		A = V*D*Vinv;

#ifdef _DEBUG
		if (!CMDCholeskyBef.empty()){
			ofstream debug_out(CMDCholeskyBef);
			vector<double> values(m_maxmodenumber+2);
			for(int n = 0; n <= m_maxmodenumber; n++){
				values[0] = D(n, n).real();
				for(int m = 0; m <= m_maxmodenumber; m++){
					values[m+1] = A(n, m).real();
				}
				PrintDebugItems(debug_out, values);
			}
		}
#endif

	}

	LLT<MatrixXcd> ldlt(A);
	MatrixXcd L = ldlt.matrixL();

	if(anm != nullptr){
		anm->resize(m_maxmodenumber+1);
		for(int n = 0; n <= m_maxmodenumber; n++){
			(*anm)[n].resize(m_maxmodenumber+1);
		}
	}

	vector<vector<complex<double>>> anmtmp;
	anmtmp.resize(m_maxmodenumber+1);
	for(int n = 0; n <= m_maxmodenumber; n++){
		anmtmp[n].resize(m_maxmodenumber+1);
	}
	complex<double> anmsc;
	double anmre, anmim;
	for(int n = 0; n <= m_maxmodenumber; n++){
		for(int m = 0; m <= m_maxmodenumber; m++){
			anmsc = L(n, m);
			anmre = anmsc.real();
			anmim = anmsc.imag();
			if(fabs(anmre) < m_cutoff){
				anmre = 0;
			}
			if(fabs(anmim) < m_cutoff){
				anmim = 0;
			}
			if(order != nullptr){
				anmtmp[n][m] = complex<double>(anmre, anmim);
			}
			else{
				anmtmp[index[n]][index[m]] = complex<double>(anmre, anmim);
			}
		}
	}
	if(anm != nullptr){
		for(int n = 0; n <= m_maxmodenumber; n++){
			for(int m = 0; m <= m_maxmodenumber; m++){
				(*anm)[n][m] = anmtmp[n][m];
			}
		}
	}

	for(int p = 0; p <= m_maxmodenumber; p++){
		AA[p] = 0;
		for(int n = 0; n <= m_maxmodenumber; n++){
			AA[p] += abs(anmtmp[n][p])*abs(anmtmp[n][p]);
		}
		index[p] = p;
	}
	sort(AA, index, m_maxmodenumber+1, false);
	m_anm.resize(m_maxmodenumber+1);
	for(int n = 0; n <= m_maxmodenumber; n++){
		m_anm[n].resize(m_maxmodenumber+1);
	}
	for(int p = 0; p <= m_maxmodenumber; p++){
		for(int n = 0; n <= m_maxmodenumber; n++){
			m_anm[n][p] = anmtmp[n][index[p]];
		}
	}

	MatrixXcd Lt = L.adjoint();
	MatrixXcd M =L*Lt-A;
	m_experr = 0;
	for(int n = 0; n <= m_maxmodenumber; n++){
		for(int m = 0; m <= m_maxmodenumber; m++){
			m_experr = max(m_experr, abs(M(n, m)));
		}
	}
	m_experr = sqrt(m_experr);
	return m_experr;
}

void HGModalDecomp::Set_anm(vector<vector<complex<double>>> *anm)
{
	m_anm.resize(m_maxmodenumber+1);
	for(int n = 0; n <= m_maxmodenumber; n++){
		m_anm[n].resize(m_maxmodenumber+1);
		for(int m = 0; m <= m_maxmodenumber; m++){
			m_anm[n][m] = (*anm)[n][m];
		}
	}
}

void HGModalDecomp::OptimizeSrcSize(double *defsrcsize, int *layer)
{
	vector<double> y(1);
	double srcsize[3];
	bool isok = true;
	int nlayer = layer != nullptr ? *layer : m_layer;

	for(int j = 0; j < 2; j++){
		m_lgrange[j].resize(m_maxmodenumber+1);
		for (int n = 0; n <= m_maxmodenumber; n++){
			m_lgrange[j][n].resize(m_maxmodenumber+1, -1);
		}
	}
	if(m_flborder.size() < m_maxmodenumber+1){
		m_flborder.resize(m_maxmodenumber+1);
	}

	if(defsrcsize == nullptr){
		m_undersrcopt = true;
		m_normsrcsize = 1.0;
		f_SetupDataGrid();
		m_calcstatus->SetSubstepNumber(nlayer, 4);

		double Wref = CostFunc(1.0, &y), Wr;
		m_calcstatus->AdvanceStep(nlayer);

		srcsize[1] = 1.0;
		while(1){
			srcsize[0] = srcsize[1]*0.5;
			Wr = CostFunc(srcsize[0], &y);
			if(Wr > Wref){
				break;
			}
			srcsize[1] = srcsize[0];
			Wref = Wr;
			if(srcsize[1] < 0.01){
				isok = false;
				break;
			}
		};
		m_calcstatus->AdvanceStep(nlayer);

		while(isok){
			srcsize[2] = srcsize[1]*2.0;
			Wr = CostFunc(srcsize[2], &y);
			if(Wr > Wref){
				break;
			}
			srcsize[1] = srcsize[2];
			Wref = Wr;
			if(srcsize[1] > 100.0){
				isok = false;
				break;
			}
		};
		m_calcstatus->AdvanceStep(nlayer);

		double optsize = 1;
		if(isok){
			BrentMethod(srcsize[0], srcsize[1], srcsize[2], 0.01, false, 1.0, &optsize, &y);
		}
		m_calcstatus->AdvanceStep(nlayer);

		m_srcsize *= optsize;
		f_SetupDataGrid(&optsize);
		m_maxmodenumber = m_maxmodecurr;
		m_undersrcopt = false;
		m_normsrcsize = 1.0;
	}
	else{
		m_srcsize = *defsrcsize;
		f_SetupDataGrid();
	}
}

void HGModalDecomp::FourierExpansion()
{
	vector<double> fr, fi;
	vector<vector<double>> frarr, fiarr, fmarr;
	double dhr = min(m_dxdq[0], m_dxdq[1]);
	double xymax[2];
	for(int j = 0; j < 2; j++){
		xymax[j] = minmax(m_xqarr[j], true);
	}
	int rmesh = (int)floor(sqrt(hypotsq(xymax[0], xymax[1]))/dhr);
	vector<double> rarr;

	for(int j = 0; j < 2; j++){
		m_fspl[j].resize(m_maxmodenumber+1);
	}
	frarr.resize(m_maxmodenumber+1);
	fiarr.resize(m_maxmodenumber+1);
	fmarr.resize(m_maxmodenumber+1);

	for(int k = 0; k <= m_maxmodenumber; k++){
		frarr[k].resize(rmesh+1);
		fiarr[k].resize(rmesh+1);
		fmarr[k].resize(rmesh+1);
	}
	rarr.resize(rmesh+1);

	for(int nr = 0; nr <= rmesh; nr++){
		rarr[nr] = dhr*(double)nr;
		FourierExpansionSingle(rarr[nr], m_maxmodenumber, &fr, &fi);
		for(int k = 0; k <= m_maxmodenumber; k++){
			frarr[k][nr] = fr[k];
			fiarr[k][nr] = fi[k];
			fmarr[k][nr] = sqrt(hypotsq(fr[k], fi[k]));
		}
	}

	for(int k = 0; k <= m_maxmodenumber; k++){
		m_fspl[0][k].SetSpline(rmesh+1, &rarr, &frarr[k]);
		m_fspl[1][k].SetSpline(rmesh+1, &rarr, &fiarr[k]);
		double fmax = minmax(fmarr[k], true);
		m_flborder[k] = rarr[rmesh];
		for(int nr = rmesh; nr >= 0; nr--){
			if(fmarr[k][nr] > 0.1*fmax){
				// pick up a "border" to separate the range by flux
				m_flborder[k] = rarr[nr];
				break;
			}
		}
	}
	m_rmax = m_r2max = rarr[rmesh];
	m_r2max *= m_r2max;

#ifdef _DEBUG
	if(!CMDFourierTheta.empty()){
		ofstream debug_out(CMDFourierTheta);
		vector<double> values(2*(m_maxmodenumber+1)+1);
		for (int nr = 0; nr <= rmesh; nr++){
			values[0] = rarr[nr];
			for (int k = 0; k <= m_maxmodenumber; k++){
				values[2*k+1] = frarr[k][nr];
				values[2*k+2] = fiarr[k][nr];
			}
			PrintDebugItems(debug_out, values);
		}
	}
#endif
}

void HGModalDecomp::FourierExpansionSingle(
	double rh, int kmax, vector<double> *fr, vector<double> *fi)
{
	int ndata = max(kmax, (int)ceil(rh/min(m_dxdq[0], m_dxdq[1])));
	int nfft = 1;
	while(nfft < ndata*8){
		nfft <<= 1;
	}

	if(nfft > m_nfftmax){
		m_ws = (double *)realloc(m_ws, sizeof(double)*nfft);
		m_nfftmax = nfft;
	}
	if(nfft != m_nfftcurr){
		if(m_fft != nullptr){
			delete m_fft;
		}
		m_fft = new FastFourierTransform(1, nfft);
		m_nfftcurr = nfft;
	}

	double dphi = PI2/(double)nfft, phi, xqh[2];

	for(int n = 0; n < nfft; n++){
		phi = dphi*(double)n;
		xqh[0] = rh*cos(phi);
		xqh[1] = rh*sin(phi);
		xqh[0] -= xqh[1]*m_zwaist;

		if(m_xqarr[0].front() > xqh[0] || m_xqarr[0].back() < xqh[0]
			|| m_xqarr[1].front() > xqh[1] || m_xqarr[1].back() < xqh[1])
		{
			m_ws[n] = 0.0;
		}
		else{
			m_ws[n] = m_fluxspl.GetValue(xqh);
		}
	}

#ifdef _DEBUG
	if(!CMDFourierPhiBef.empty()){
		ofstream debug_out(CMDFourierPhiBef);
		vector<double> wsl(2);
		for (int n = 0; n < nfft; n++){
			wsl[0] = dphi*(double)n;
			wsl[1] = m_ws[n];
			PrintDebugItems(debug_out, wsl);
		}
	}
#endif

	if(fr->size() <= kmax){
		fr->resize(kmax+1);
	}
	if(fi->size() <= kmax){
		fi->resize(kmax+1);
	}

	m_fft->DoRealFFT(m_ws);
	for(int k = 0; k <= kmax; k++){
		(*fr)[k] = m_ws[2*k]*dphi;
		if(k == 0){
			(*fi)[k] = 0;
		}
		else{
			(*fi)[k] = -m_ws[2*k+1]*dphi;
			// take the complex conjugate
		}
	}

#ifdef _DEBUG
	if(!CMDFourierPhiAft.empty()){
		ofstream debug_out(CMDFourierPhiAft);
		vector<double> wsl(3);
		for (int k = 0; k <= kmax; k++){
			wsl[0] = k;
			wsl[1] = (*fr)[k];
			wsl[2] = (*fi)[k];
			PrintDebugItems(debug_out, wsl);
		}
	}
#endif
}

double HGModalDecomp::GetWignerAt(int p, vector<vector<complex<double>>> *ws,
		int posxy, int posxyq, int nmesh, int anmesh,
		vector<vector<complex<double>>> *anm, vector<vector<int>> *mode)
{
	int n, m;
	complex<double> Wr(0.0, 0.0), Wrrc;

	Wr = complex<double>(0.0, 0.0);
	for(n = 0; n < (*anm)[p].size(); n++){
		for(m = 0; m < (*anm)[p].size(); m++){
			Wrrc = (*ws)[(*mode)[p][n]*(m_maxmodenumber+1)+(*mode)[p][m]][posxy*anmesh+posxyq]*(*anm)[p][n]*conj((*anm)[p][m]); 
			Wr = Wr+Wrrc;
		}
	}
	return Wr.real();
}

void HGModalDecomp::DumpFieldProfile(const char *bufbin, 
	double eps, int pmax, double dxy, bool iswrite, 
	vector<double> &xyarr, vector<vector<double>> &datar, vector<vector<double>> &datai)
{
	vector<vector<complex<double>>> Ea;

	pmax = GetMaxOrder(pmax);

	int mesh = (int)floor(0.5+max(fabs(m_XQarr[0].back()), fabs(m_XQarr[0].front()))/dxy);
	xyarr.resize(2*mesh+1);
	for(int n = -mesh; n <= mesh; n++){
		xyarr[n+mesh] = dxy*n;
	}
	mesh = 2*mesh+1;
	GetComplexAmp(xyarr, &Ea, eps, pmax, false, nullptr, nullptr);
	if(bufbin != nullptr){
		f_ExportFieldBinary(bufbin, &xyarr, &Ea);
	}

	if(iswrite){
		datar.resize(pmax+1);
		datai.resize(pmax+1);
		for(int p = 0; p <= pmax; p++){
			datar[p].resize(mesh);
			datai[p].resize(mesh);
			for(int n = 0; n < mesh; n++){
				datar[p][n] = Ea[p][n].real();
				datai[p][n] = Ea[p][n].imag();
			}
		}
	}
}

void HGModalDecomp::WriteResults(string &result, double cmderr[])
{
	int nmodes = m_maxmodenumber+1;
	vector<double> anmre(nmodes*nmodes), anmim(nmodes*nmodes);
	for(int n = 0; n < nmodes; n++){
		for(int m = 0; m < nmodes; m++){
			int nm = n*nmodes+m;
			anmre[nm] = m_anm[n][m].real();
			anmim[nm] = m_anm[n][m].imag();
		}
	}

	stringstream ssresult;
	ssresult << "{" << endl;
	WriteJSONValue(ssresult, JSONIndent, m_maxmodenumber, MaxOrderLabel.c_str(), false, true);
	WriteJSONValue(ssresult, JSONIndent, m_lambda, WavelengthLabel.c_str(), false, true);
	WriteJSONValue(ssresult, JSONIndent, m_srcsize, SrcSizeLabel.c_str(), false, true);
	WriteCommonJSON(ssresult, cmderr, nmodes, m_norm_factor, anmre, anmim);
	
	result = ssresult.str();
}

void HGModalDecomp::LoadResults(int maxorder, 
	double srcsize, double fnorm, vector<double> &anmre, vector<double> &anmim)
{
	m_maxmodenumber = maxorder;
	m_srcsize = srcsize;
	m_norm_factor = fnorm;
	int nmodes = m_maxmodenumber+1;
	m_anm.resize(nmodes);
	for(int n = 0; n < nmodes; n++){
		m_anm[n].resize(nmodes);
		for(int m = 0; m < nmodes; m++){
			int nm = n*nmodes+m;
			m_anm[n][m] = complex<double>(anmre[nm], anmim[nm]);
		}
	}
	CreateHGMode();
}

//----- private functions -----
void HGModalDecomp::f_SetupDataGrid(double *ladj)
{
	if(ladj != nullptr){
		m_xqarr[0] /= *ladj;
		m_dxdq[0] /= *ladj;
		m_xqarr[1] *= *ladj;
		m_dxdq[1] *=  *ladj;
		m_zwaist /= (*ladj)*(*ladj);
	}
	else{
		double sigpi = 2.0*SQRTPI*m_srcsize;
		m_xqarr[0] /= sigpi;
		m_dxdq[0] /= sigpi;
		m_xqarr[1] *= sigpi/m_lambda;
		m_dxdq[1] *=  sigpi/m_lambda;
		m_zwaist *= m_lambda/sigpi/sigpi;
	}

	m_fluxspl.SetSpline2D(m_mesh, &m_xqarr[0], &m_xqarr[1], &m_data, false);
	m_norm_factor = m_fluxspl.Integrate();
}

void HGModalDecomp::f_ComputeWholeWigner(double fnorm, int indices[], int ixy, int iq, 
		vector<complex<double>> *aAnm, vector<int> *nindex, vector<int> *mindex, 
		vector<vector<complex<double>>> *ws, vector<double> &data,
		int rank, int mpiprocesses)
{
	int mesh[2], nxy, nq, n, m;
	complex<double> Wrrc;

	for(int j = 0; j < 2; j++){
		mesh[j] = (int)m_xqarr[j].size();
	}

	vector<int> steps, inistep, finstep;
	mpi_steps(mesh[0], mesh[1], mpiprocesses, &steps, &inistep, &finstep);

	m_calcstatus->SetSubstepNumber(m_layer, steps[0]);

	for(nxy = 0; nxy < mesh[0]; nxy++){
		indices[ixy] = nxy;
		for(nq = 0; nq < mesh[1]; nq++){
			indices[iq] = nq;

			int nm = nxy*mesh[1]+nq;
			if (nm < inistep[rank] || nm > finstep[rank]){
				continue;
			}

			int iindex = m_wig4d->GetTotalIndex(indices);
			double dbldr = 0;
			data[iindex] = 0.0;
			for(nm = 0; nm < aAnm->size(); nm++){
				n = (*nindex)[nm];
				m = (*mindex)[nm];
				Wrrc = (*ws)[n*(m_maxmodenumber+1)+m][nxy*mesh[1]+nq]*(*aAnm)[nm];
				dbldr += Wrrc.real();
			}
			data[iindex] = (double)(fnorm*dbldr);
			m_calcstatus->AdvanceStep(m_layer);
		}
	}

	if(mpiprocesses > 1){
		for(nxy = 0; nxy < mesh[0]; nxy++){
			indices[ixy] = nxy;
			for(nq = 0; nq < mesh[1]; nq++){
				indices[iq] = nq;
				int iindex = m_wig4d->GetTotalIndex(indices);
				int nm = nxy*mesh[1]+nq;
				int currrank;
				for(currrank = 0; currrank < mpiprocesses; currrank++){
					if(nm >= inistep[currrank] && nm <= finstep[currrank]){
						break;
					}
				}
				MPI_Bcast(&data[iindex], 1, MPI_DOUBLE, currrank, MPI_COMM_WORLD);
			}
		}
	}
}

void HGModalDecomp::f_ExportFieldBinary(const char *buffer, 
			vector<double> *xyarr, vector<vector<complex<double>>> *Ea)
{
	int nmesh[2];
	double dxy, *datar, *datai;

	nmesh[0] = (int)Ea->size();
	nmesh[1] = (int)xyarr->size();
	dxy = (xyarr->back()-xyarr->front())/(double)(nmesh[1]-1);

	FILE *fp = fopen(buffer, "wb");

	fwrite(nmesh, sizeof(int), 2, fp);
	fwrite(&dxy, sizeof(double), 1, fp);

	datar = new double[nmesh[1]];
	datai = new double[nmesh[1]];

	for(int p = 0; p < nmesh[0]; p++){
		for(int nx = 0; nx < nmesh[1]; nx++){
			datar[nx] = (*Ea)[p][nx].real();
			datai[nx] = (*Ea)[p][nx].imag();
		}
		fwrite(datar, sizeof(double), nmesh[1], fp);
		fwrite(datai, sizeof(double), nmesh[1], fp);
	}
	fclose(fp);

	delete[] datar;
	delete[] datai;
}

void HGModalDecomp::f_AssignWignerArray(
	vector<vector<complex<double>>> *ws, vector<double> *xyarr, vector<double> *qarr)
{
	int mesh[2], n, m, nxy, nq;
	double Wana[2];

	mesh[0] = (int)xyarr->size();
	mesh[1] = (int)qarr->size();

	int nmodes = (m_maxmodenumber+1)*(m_maxmodenumber+1);
	ws->resize(nmodes);
	for(int n = 0; n < nmodes; n++){
		(*ws)[n].resize(mesh[0]*mesh[1]);
	}

	m_calcstatus->SetSubstepNumber(m_layer, (m_maxmodenumber+1)*(m_maxmodenumber+1));
	for(n = 0; n <= m_maxmodenumber; n++){
		for(m = 0; m <= m_maxmodenumber; m++){
			for(nxy = 0; nxy < mesh[0]; nxy++){
				for(nq = 0; nq < mesh[1]; nq++){
					m_hgmode->GetWigner(n, m, (*xyarr)[nxy], (*qarr)[nq], Wana);
					(*ws)[n*(m_maxmodenumber+1)+m][nxy*mesh[1]+nq] = complex<double>(Wana[0], Wana[1]);
				}
			}
			m_calcstatus->AdvanceStep(m_layer);
		}
	}		
}

//-----------
HGModalDecomp2D::HGModalDecomp2D(
	PrintCalculationStatus *calcstatus, int maxmodes[], int cmdmode, double cutoff, Wigner4DManipulator *wig4d)
{
	m_calcstatus = calcstatus;
	for(int j = 0; j < 2; j++){
		m_hgmode[j] = nullptr;
		m_maxmode[j] = maxmodes[j];
		m_normsrcsize[j] = 1.0;
	}
	m_hgmode[2] = nullptr;
	m_max_cmdmode = cmdmode;
	m_wig4d = wig4d;
	m_lambda = m_wig4d->GetWavelength();
	m_cutoff = cutoff;

	for(int j = 0; j < 2; j++){
		m_hgmode[j] = new HGModalDecomp(2, m_calcstatus, m_maxmode[j], cutoff, wig4d);
	}
}

HGModalDecomp2D::~HGModalDecomp2D()
{
	for(int j = 0; j < 3; j++){
		if(m_hgmode[j] != nullptr){
			delete m_hgmode[j];
		}
	}
}

void HGModalDecomp2D::LoadData()
{
	for(int j = 0; j < 2; j++){
		m_wig4d->GetXYQArray(j, m_xyarr[j], m_qarr[j]);
		m_xyarr[j] *= 1.0e-3; // mm -> m
		m_qarr[j] *= 1.0e-3; // mrad -> rad
		m_nmesh[j] = (int)m_xyarr[j].size();
		m_anmesh[j] = (int)m_qarr[j].size();
	}
}

void HGModalDecomp2D::ComputePrjBeamParameters(double *sigma)
{
	vector<vector<double>> dprj;
	vector<vector<double>> xyq(2);
	double *sigmain = nullptr;
	double defadj = 1.0;
	int sublayer = 1;

	for(int j = 0; j < 2; j++){
		m_wig4d->GetSliceValues(j, nullptr, dprj);
		m_wig4d->GetXYQArray(j, xyq[0], xyq[1]);
		m_hgmode[j]->AssingData(&xyq, dprj, true);
		if(sigma != nullptr){
			sigmain = &sigma[j];
		}
		m_hgmode[j]->OptimizeSrcSize(sigmain, &sublayer);
		m_srcsize[j] = m_hgmode[j]->GetSigma();
		m_maxmode[j] = m_hgmode[j]->GetMaxOrder(m_maxmode[j]);
		dprj.clear();
		if(sigma == nullptr){
			m_calcstatus->AdvanceStep(0);
		}
	}
}

void HGModalDecomp2D::GetAnmAt(int jxy, int posidx[], vector<vector<complex<double>>> *Anm)
{
	vector<vector<double>> dprj;

	m_wig4d->GetSliceValues(jxy, posidx, dprj);
	m_hgmode[jxy]->AssingData(nullptr, dprj, false);
	m_hgmode[jxy]->FourierExpansion();
	m_hgmode[jxy]->GetAnm(Anm);
}

void HGModalDecomp2D::GetAnmAll(int jxy, int rank, int mpiprocesses)
{
	MPI_Status mpistatus;

	int posidx[2];
	int kxy = 1-jxy;

	vector<vector<complex<double>>> Anm;
	vector<vector<vector<double>>> mnRe, mnIm;

	int nmodes[2], totalmodes;
	nmodes[0] = m_maxmode[jxy]+1; 
	nmodes[1] = m_maxmode[kxy]+1; 
	totalmodes = nmodes[0]*nmodes[0];
	mnRe.resize(totalmodes);
	mnIm.resize(totalmodes);
	for(int n = 0; n < totalmodes; n++){
		mnRe[n].resize(m_nmesh[kxy]);
		mnIm[n].resize(m_nmesh[kxy]);
		for(posidx[0] = 0; posidx[0] < m_nmesh[kxy]; posidx[0]++){
			mnRe[n][posidx[0]].resize(m_anmesh[kxy]);
			mnIm[n][posidx[0]].resize(m_anmesh[kxy]);
		}
	}

	m_normfactor = m_hgmode[jxy]->GetNormalization();

	double *anmtmp;
	if(mpiprocesses > 1){
		anmtmp = new double[m_nmesh[kxy]*m_anmesh[kxy]*totalmodes*2];
	}

	vector<int> steps, inistep, finstep;
	mpi_steps(m_nmesh[kxy], m_anmesh[kxy], mpiprocesses, &steps, &inistep, &finstep);

	m_calcstatus->SetSubstepNumber(1, steps[0]);
	for(posidx[0] = 0; posidx[0] < m_nmesh[kxy]; posidx[0]++){
		for(posidx[1] = 0; posidx[1] < m_anmesh[kxy]; posidx[1]++){
			int totpos = posidx[0]*m_anmesh[kxy]+posidx[1];
			if(totpos < inistep[rank] || totpos > finstep[rank]){
				continue;
			}
			GetAnmAt(jxy, posidx, &Anm);
			for(int n = 0; n < nmodes[0]; n++){
				for(int m = 0; m < nmodes[0]; m++){
					mnRe[n*nmodes[0]+m][posidx[0]][posidx[1]] = Anm[n][m].real();
					mnIm[n*nmodes[0]+m][posidx[0]][posidx[1]] = Anm[n][m].imag();
					if(mpiprocesses > 1){
						int ntlt = (posidx[0]*m_anmesh[kxy]+posidx[1])*totalmodes;
						ntlt += n*nmodes[0]+m;
						anmtmp[ntlt*2] = Anm[n][m].real();
						anmtmp[ntlt*2+1] = Anm[n][m].imag();
					}
				}
			}
			m_calcstatus->AdvanceStep(1);
		}
	}

	if(mpiprocesses > 1){
		for(int k = 1; k < mpiprocesses; k++){
			if(rank == 0){
				MPI_Recv(anmtmp+inistep[k]*totalmodes*2, steps[k]*totalmodes*2, MPI_DOUBLE, k, 0, MPI_COMM_WORLD, &mpistatus);
			}
			else if(rank == k){
				MPI_Send(anmtmp+inistep[k]*totalmodes*2, steps[k]*totalmodes*2, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
			}
			MPI_Barrier(MPI_COMM_WORLD);
		}
		MPI_Bcast(anmtmp, m_nmesh[kxy]*m_anmesh[kxy]*totalmodes*2, MPI_DOUBLE, 0, MPI_COMM_WORLD);
		for(posidx[0] = 0; posidx[0] < m_nmesh[kxy]; posidx[0]++){
			for(posidx[1] = 0; posidx[1] < m_anmesh[kxy]; posidx[1]++){
				for(int n = 0; n < nmodes[0]; n++){
					for(int m = 0; m < nmodes[0]; m++){
						int ntlt = (posidx[0]*m_anmesh[kxy]+posidx[1])*totalmodes;
						ntlt += n*nmodes[0]+m;
						mnRe[n*nmodes[0]+m][posidx[0]][posidx[1]] = anmtmp[ntlt*2];
						mnIm[n*nmodes[0]+m][posidx[0]][posidx[1]] = anmtmp[ntlt*2+1];
					}
				}
			}
		}
		delete[] anmtmp;
	}
	m_calcstatus->AdvanceStep(0);

	totalmodes = nmodes[1]*nmodes[1];
	if(mpiprocesses > 1){
		anmtmp = new double[nmodes[0]*nmodes[0]*totalmodes*2];
	}

#ifdef _DEBUG
	if(rank == 0 && !CMD_Anm_Func_1st.empty()){
		vector<int> modecheck {0, 5, 10};
		ofstream debug_out(CMD_Anm_Func_1st);
		vector<string> items(2);
		items[0] = "xy";
		items[1] = "q";
		for (int n = 0; n < modecheck.size(); n++){
			for (int m = 0; m < modecheck.size(); m++){
				if (modecheck[n] > m_maxmode[0] || modecheck[m] > m_maxmode[1]){
					continue;
				}
				stringstream ss;
				ss << "N" <<modecheck[n] << modecheck[m];
				items.push_back(ss.str());
			}
		}
		PrintDebugItems(debug_out, items);

		vector<double> xy, q, values(items.size());
		m_wig4d->GetXYQArray(kxy, xy, q);
		for (posidx[0] = 0; posidx[0] < m_nmesh[kxy]; posidx[0]++){
			for (posidx[1] = 0; posidx[1] < m_anmesh[kxy]; posidx[1]++){
				values[0] = xy[posidx[0]];
				values[1] = q[posidx[1]];
				int nm = 1;
				for (int n = 0; n < modecheck.size(); n++){
					for (int m = 0; m < modecheck.size(); m++){
						if (modecheck[n] > m_maxmode[0] || modecheck[m] > m_maxmode[1]){
							continue;
						}
						values[++nm] = mnRe[modecheck[n]*nmodes[0]+modecheck[m]][posidx[0]][posidx[1]];
					}
				}
				PrintDebugItems(debug_out, values);
			}
		}
		debug_out.close();
	}
#endif

	m_Anm.resize(nmodes[0]*nmodes[1]);
	for(int nm = 0; nm < nmodes[0]*nmodes[1]; nm++){
		m_Anm[nm].resize(nmodes[0]*nmodes[1]);
	}

	vector<vector<complex<double>>> AnmRe, AnmIm;
	int nnk, mmk;

	mpi_steps(nmodes[0], nmodes[0], mpiprocesses, &steps, &inistep, &finstep);

	m_calcstatus->SetSubstepNumber(1, steps[0]);

	double Asum = 0;
	m_hgmode[kxy]->SetNormalization(1.0);
	for(int n = 0; n < nmodes[0]; n++){
		for(int m = 0; m < nmodes[0]; m++){
			int nm = n*nmodes[0]+m;
			if(nm < inistep[rank] || nm > finstep[rank]){
				continue;
			}
			m_hgmode[kxy]->AssingData(nullptr, mnRe[n*nmodes[0]+m], false);
			m_hgmode[kxy]->FourierExpansion();
			m_hgmode[kxy]->GetAnm(&AnmRe);

			m_hgmode[kxy]->AssingData(nullptr, mnIm[n*nmodes[0]+m], false);
			m_hgmode[kxy]->FourierExpansion();
			m_hgmode[kxy]->GetAnm(&AnmIm);

			for(int nk = 0; nk < nmodes[1]; nk++){
				for(int mk = 0; mk < nmodes[1]; mk++){
					if(jxy == 0){
						nnk = n*nmodes[1]+nk;
						mmk = m*nmodes[1]+mk;
					}
					else{
						nnk = nk*nmodes[0]+n;
						mmk = mk*nmodes[0]+m;
					}
					m_Anm[nnk][mmk] = (AnmRe[nk][mk]+complex<double>(0.0, 1.0)*AnmIm[nk][mk]);
					if(mpiprocesses > 1){
						int ntlt = (n*nmodes[0]+m)*totalmodes;
						ntlt += nk*nmodes[1]+mk;
						anmtmp[ntlt*2] = m_Anm[nnk][mmk].real();
						anmtmp[ntlt*2+1] = m_Anm[nnk][mmk].imag();
					}
					if(nnk == mmk){
						Asum += m_Anm[nnk][mmk].real();
					}
				}
			}
			m_calcstatus->AdvanceStep(1);
		}
	}

	if(mpiprocesses > 1){
		for(int k = 1; k < mpiprocesses; k++){
			if(rank == 0){
				MPI_Recv(anmtmp+inistep[k]*totalmodes*2, steps[k]*totalmodes*2, MPI_DOUBLE, k, 0, MPI_COMM_WORLD, &mpistatus);
			}
			else if(rank == k){
				MPI_Send(anmtmp+inistep[k]*totalmodes*2, steps[k]*totalmodes*2, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
			}
			MPI_Barrier(MPI_COMM_WORLD);
		}
		MPI_Bcast(anmtmp, nmodes[0]*nmodes[0]*totalmodes*2, MPI_DOUBLE, 0, MPI_COMM_WORLD);
		for(int n = 0; n < nmodes[0]; n++){
			for(int m = 0; m < nmodes[0]; m++){
				for(int nk = 0; nk < nmodes[1]; nk++){
					for(int mk = 0; mk < nmodes[1]; mk++){
						if(jxy == 0){
							nnk = n*nmodes[1]+nk;
							mmk = m*nmodes[1]+mk;
						}
						else{
							nnk = nk*nmodes[0]+n;
							mmk = mk*nmodes[0]+m;
						}
						int ntlt = (n*nmodes[0]+m)*totalmodes;
						ntlt += nk*nmodes[1]+mk;
						m_Anm[nnk][mmk] = complex<double>(anmtmp[ntlt*2], anmtmp[ntlt*2+1]);
					}	
				}
			}
		}
		delete[] anmtmp;
	}

	m_calcstatus->AdvanceStep(0);

#ifdef _DEBUG
	if(rank == 0 && !CMD_Anm_Func_2nd.empty()){
		ofstream debug_out(CMD_Anm_Func_2nd);
		vector<double> values(4);

		vector<string> items(4);
		items[0] = "n";
		items[1] = "m";
		items[2] = "Real";
		items[3] = "Imag";
		PrintDebugItems(debug_out, items);

		for (int n = 0; n < nmodes[0]*nmodes[1]; n++){
			for (int m = 0; m < nmodes[0]*nmodes[1]; m++){
				values[0] = n;
				values[1] = m;
				values[2] = m_Anm[n][m].real();
				values[3] = m_Anm[n][m].imag();
				PrintDebugItems(debug_out, values);
			}
		}
	}
#endif

	m_hgmode[2] = new HGModalDecomp(2, m_calcstatus, nmodes[0]*nmodes[1]-1, m_cutoff, m_wig4d);
	m_hgmode[2]->SetAnm(&m_Anm);
	m_experr = m_hgmode[2]->CholeskyDecomp(&m_anm, &m_ordered_mode);
}

void HGModalDecomp2D::GetComplexAmp2D(vector<vector<double>> &xyarr,
		vector<vector<vector<complex<double>>>> *Ea, double eps, int pmax,
		vector<vector<complex<double>>> *anm, vector<vector<int>> *hindex, vector<vector<int>> *jindex,
		int rank, int mpiprocesses)
{
	int nxy[2], mode[2], nmodes[2], mesh[2], totalmodes;
	vector<vector<complex<double>>> Exyarr[2];
	complex<double> Exy[2];

	for(int j = 0; j < 2; j++){
		mesh[j] = (int)xyarr[j].size();
	}
	for(int j = 0; j < 2; j++){
		m_hgmode[j]->GetComplexAmp(xyarr[j], &Exyarr[j], 0.0, -1, true);
		nmodes[j] = m_maxmode[j]+1;
	}
	totalmodes = nmodes[0]*nmodes[1];

	if(anm != nullptr){
		pmax = (int)anm->size()-1;
	}
	else{
		pmax = m_hgmode[2]->GetMaxOrder(pmax);
	}
	if(pmax < 0){
		pmax = totalmodes-1;
	}
	else{
		pmax = min(totalmodes-1, pmax);
	}

	Ea->resize(pmax+1);
	for(int p = 0; p <= pmax; p++){
		(*Ea)[p].resize(mesh[0]);
		for(nxy[0] = 0; nxy[0] < mesh[0]; nxy[0]++){
			(*Ea)[p][nxy[0]].resize(mesh[1]);
		}
	}

	vector<int> steps, inistep, finstep;
	mpi_steps(mesh[0], mesh[1], mpiprocesses, &steps, &inistep, &finstep);
	m_calcstatus->SetSubstepNumber(1, steps[0]);

	int q;
	for(nxy[0] = 0; nxy[0] < mesh[0]; nxy[0]++){
		for(nxy[1] = 0; nxy[1] < mesh[1]; nxy[1]++){
			int nm = nxy[1]*mesh[0]+nxy[0];
			if(nm < inistep[rank] || nm > finstep[rank]){
				continue;
			}
			for(int p = 0; p <= pmax; p++){
				(*Ea)[p][nxy[0]][nxy[1]] = complex<double>(0.0, 0.0);
				if(anm != nullptr){
					for(int m = 0; m < (*anm)[p].size(); m++){
						mode[0] = (*hindex)[p][m];
						mode[1] = (*jindex)[p][m];
						for(int j = 0; j < 2; j++){
							Exy[j] = Exyarr[j][mode[j]][nxy[j]];
						}
						(*Ea)[p][nxy[0]][nxy[1]] += (*anm)[p][m]*Exy[0]*Exy[1];
					}
				}
				else{
					for(int qr = 0; qr < totalmodes; qr++){
						q = GetOrderedModeNumber(qr);
						mode[0] = q/nmodes[1];
						mode[1] = q%nmodes[1];
						for(int j = 0; j < 2; j++){
							Exy[j] = Exyarr[j][mode[j]][nxy[j]];
						}
						if(abs(m_anm[qr][p]) > eps){
							(*Ea)[p][nxy[0]][nxy[1]] += m_anm[qr][p]*Exy[0]*Exy[1];
						}
					}
				}
			}
			m_calcstatus->AdvanceStep(1);
		}
	}

	if(mpiprocesses > 1){
		double *ws = new double[2*(pmax+1)];
		for (nxy[0] = 0; nxy[0] < mesh[0]; nxy[0]++){
			for (nxy[1] = 0; nxy[1] < mesh[1]; nxy[1]++){
				int nm = nxy[1]*mesh[0]+nxy[0];
				int currrank;
				for(currrank = 0; currrank < mpiprocesses; currrank++){
					if(nm >= inistep[currrank] && nm <= finstep[currrank]){
						break;
					}
				}
				if(currrank == rank){
					for (int p = 0; p <= pmax; p++){
						ws[2*p] = (*Ea)[p][nxy[0]][nxy[1]].real();
						ws[2*p+1] = (*Ea)[p][nxy[0]][nxy[1]].imag();
					}
				}
				MPI_Bcast(ws, 2*(pmax+1), MPI_DOUBLE, currrank, MPI_COMM_WORLD);
				if(currrank != rank){
					for (int p = 0; p <= pmax; p++){
						(*Ea)[p][nxy[0]][nxy[1]] = complex<double>(ws[2*p], ws[2*p+1]);
					}
				}
			}
		}
		delete[] ws;
	}
}

void HGModalDecomp2D::DumpFieldProfile(const char *bufbin, 
	double eps, int pmax, double dxy[], bool iswrite,
	vector<vector<double>> &xyarr, vector<vector<double>> &datar, vector<vector<double>> &datai,
	int rank, int mpiprocess)
{
	vector<vector<vector<complex<double>>>> Ea;

	int mesh[2];
	xyarr.resize(2);

	for(int j = 0; j < 2; j++){
		mesh[j] = (int)floor(0.5+max(fabs(m_xyarr[j].back()), fabs(m_xyarr[j].front()))/dxy[j]);
		xyarr[j].resize(2*mesh[j]+1);
		for(int n = -mesh[j]; n <= mesh[j]; n++){
			xyarr[j][n+mesh[j]] = dxy[j]*n;
		}
		mesh[j] = 2*mesh[j]+1;
	}

	pmax = m_hgmode[2]->GetMaxOrder(pmax);
	GetComplexAmp2D(xyarr, &Ea, eps, pmax, nullptr, nullptr, nullptr, rank, mpiprocess);
	if(bufbin != nullptr){
		f_ExportFieldBinary(bufbin, &xyarr, &Ea);
	}

	if(iswrite){
		datar.resize(pmax+1);
		datai.resize(pmax+1);
		for(int p = 0; p <= pmax; p++){
			datar[p].resize(mesh[0]*mesh[1]);
			datai[p].resize(mesh[0]*mesh[1]);
			for(int n = 0; n < mesh[0]; n++){
				for (int m = 0; m < mesh[1]; m++){
					int nm = m*mesh[0]+n;
					datar[p][nm] = Ea[p][n][m].real();
					datai[p][nm] = Ea[p][n][m].imag();
				}
			}
		}
	}
}

double HGModalDecomp2D::GetNormalizeFactor()
{
	return m_normfactor/(m_srcsize[0]*m_srcsize[1]*PI*4.0);
}

void HGModalDecomp2D::GetFluxConsistency(int pmax, double eps, vector<double> &fa)
{
	m_hgmode[2]->GetFluxConsistency(pmax, eps, fa);
}

void HGModalDecomp2D::ReconstructExport(int pmax, double epsanm, 
		double *CMDerr, vector<vector<vector<double>>> &data, int rank, int mpiprocesses)
{
	vector<double> stderror[NumberWigError];
	double errors[NumberWigError];
	int nxy[2], nq[2], nmodes = (m_maxmode[0]+1)*(m_maxmode[1]+1);
	double xy[2], q[2], degcoh;
	double fnorm = GetNormalizeFactor();

	int rep = 0, n, m;
	double Wana[2];

	for(int j = 0; j < 2; j++){
		int nrmodes = (m_maxmode[j]+1)*(m_maxmode[j]+1);
		m_ws[j].resize(nrmodes);
		for(int n = 0; n < nrmodes; n++){
			m_ws[j][n].resize(m_nmesh[j]*m_anmesh[j]);
		}
	}

	m_calcstatus->SetSubstepNumber(1, m_maxmode[0]*m_maxmode[1]*2);

	for(int j = 0; j < 2; j++){
		for(n = 0; n <= m_maxmode[j]; n++){
			for(m = 0; m <= m_maxmode[j]; m++){
				for(nxy[j] = 0; nxy[j] < m_nmesh[j]; nxy[j]++){
					xy[j] = m_xyarr[j][nxy[j]];
					for(nq[j] = 0; nq[j] < m_anmesh[j]; nq[j]++){
						q[j] = m_qarr[j][nq[j]];
						m_hgmode[j]->GetHGMode()->GetWigner(n, m, xy[j], q[j], Wana);
						m_ws[j][m+n*(m_maxmode[j]+1)][nxy[j]*m_anmesh[j]+nq[j]] 
							= complex<double>(Wana[0], Wana[1]);
					}
				}
			}	
			m_calcstatus->AdvanceStep(1);
		}
	}
	m_calcstatus->AdvanceStep(0);

	m_hgmode[2]->GetApproximatedAnm(pmax, epsanm, &m_Anm_approx, &m_nindex, &m_mindex);

	int tmesh = m_nmesh[0]*m_nmesh[1]*m_anmesh[0]*m_anmesh[1];
	vector<double> wigdata(tmesh);
	f_ComputeWholeWigner(fnorm, wigdata, rank, mpiprocesses);

	data.resize(2);
	Wigner4DManipulator wigmanip;
	vector<vector<double>> varxy {m_xyarr[0], m_xyarr[1], m_qarr[0], m_qarr[1]};
	for(int j = 0; j < 4; j++){
		varxy[j] *= 1.0e+3; // m,rad -> mm,mrad
	}
	wigmanip.SetWavelength(m_lambda);
	wigmanip.LoadData(menu::XXpYYp, varxy, wigdata);
	
	vector<vector<double>> data2d[2];
	for(int j = 0; j < 2; j++){
		data[j].resize(2);
		for(int i = 0; i < 2; i++){
			data2d[i].clear();
		}
		m_wig4d->GetSliceValues(j, nullptr, data2d[0]);
		wigmanip.GetSliceValues(j, nullptr, data2d[1]);
		for(int i = 0; i < 2; i++){
			data[j][i].resize(m_nmesh[j]*m_anmesh[j]);
			for(int n = 0; n < m_nmesh[j]; n++){
				for (int m = 0; m < m_anmesh[j]; m++){
					data[j][i][m*m_nmesh[j]+n] = data2d[i][n][m];
				}
			}
		}
	}

	m_wig4d->GetCoherenceDeviation(&degcoh, errors, wigdata);
	*CMDerr = errors[WigErrorDeviation];
	
	m_calcstatus->AdvanceStep(0);	
}

double HGModalDecomp2D::GetWignerAt(int posxy[], int posxyq[], int nmesh[], int anmesh[])
{
	int n, m, h, k, j, l, nm;
	complex<double> Wr(0.0, 0.0), Wrrc;

	Wr = complex<double>(0.0, 0.0);

	for(nm = 0; nm < m_Anm_approx.size(); nm++){
		n = GetOrderedModeNumber(m_nindex[nm]);
		m = GetOrderedModeNumber(m_mindex[nm]);
		h = n/(m_maxmode[1]+1);
		j = n%(m_maxmode[1]+1);
		k = m/(m_maxmode[1]+1);
		l = m%(m_maxmode[1]+1);
		Wrrc = m_ws[0][h*(m_maxmode[0]+1)+k][posxy[0]*anmesh[0]+posxyq[0]]
			  *m_ws[1][j*(m_maxmode[1]+1)+l][posxy[1]*anmesh[1]+posxyq[1]]
			  *m_Anm_approx[nm];
		Wr = Wr+Wrrc;
	}
	return Wr.real();
}

int HGModalDecomp2D::GetOrderedModeNumber(int seqno)
{
	if(m_ordered_mode.size() == 0){
		return seqno;
	}
	return m_ordered_mode[seqno];
}

void HGModalDecomp2D::WriteResults(string &result, double cmderr[])
{
	int nmodes = (m_maxmode[0]+1)*(m_maxmode[1]+1);
	vector<double> anmre(nmodes*nmodes), anmim(nmodes*nmodes);
	for(int n = 0; n < nmodes; n++){
		for(int m = 0; m < nmodes; m++){
			int nm = n*nmodes+m;
			anmre[nm] = m_anm[n][m].real();
			anmim[nm] = m_anm[n][m].imag();
		}
	}

	stringstream ssresult;
	vector<double> srcsize(2);
	vector<int> maxorder(2);
	for(int j = 0; j < 2; j++){
		srcsize[j] = m_srcsize[j];
		maxorder[j] = m_maxmode[j];
	}
	
	ssresult << "{" << endl;
	WriteJSONArray(ssresult, JSONIndent, maxorder, MaxOrderLabel.c_str(), false, true);
	WriteJSONValue(ssresult, JSONIndent, m_lambda, WavelengthLabel.c_str(), false, true);
	WriteJSONArray(ssresult, JSONIndent, srcsize, SrcSizeLabel.c_str(), false, true);
	WriteJSONArray(ssresult, JSONIndent, m_ordered_mode, OrderLabel.c_str(), false, true);
	WriteCommonJSON(ssresult, cmderr, nmodes, m_normfactor, anmre, anmim);
	
	result = ssresult.str();
}

void HGModalDecomp2D::LoadResults(int maxorder[], double srcsize[], 
	double fnorm, vector<int> &order, vector<double> &anmre, vector<double> &anmim)
{
	for(int j = 0; j < 2; j++){
		m_srcsize[j] = srcsize[j];
		m_maxmode[j] = maxorder[j];
	}
	m_ordered_mode = order;
	int nmodes = (m_maxmode[0]+1)*(m_maxmode[1]+1);
	m_anm.resize(nmodes);
	for(int n = 0; n < nmodes; n++){
		m_anm[n].resize(nmodes);
		for(int m = 0; m < nmodes; m++){
			int nm = n*nmodes+m;
			m_anm[n][m] = complex<double>(anmre[nm], anmim[nm]);
		}
	}
	m_normfactor = fnorm;

	ComputePrjBeamParameters(m_srcsize);
	for(int j = 0; j < 2; j++){
		m_hgmode[j]->SetMaximumModeNumber(m_maxmode[j]);
		m_hgmode[j]->CreateHGMode();
	}
	m_hgmode[2] = new HGModalDecomp(2, m_calcstatus, nmodes-1, m_cutoff, m_wig4d);
	m_hgmode[2]->Set_anm(&m_anm);
}

//---------- private functions
void HGModalDecomp2D::f_ExportFieldBinary(const char *buffer, 
		vector<vector<double>> *xyarr, vector<vector<vector<complex<double>>>> *Ea)
{
	int nmesh[3];
	double dxy[2], *datar, *datai;

	nmesh[0] = (int)Ea->size();
	for(int j = 0; j < 2; j++){
		nmesh[j+1] = (int)(*xyarr)[j].size();
		dxy[j] = ((*xyarr)[j].back()-(*xyarr)[j].front())/(double)(nmesh[j]-1);
	}

	FILE *fp = fopen(buffer, "wb");
	fwrite(nmesh, sizeof(int), 3, fp);
	fwrite(dxy, sizeof(double), 2, fp);

	datar = new double[nmesh[0]*nmesh[1]];
	datai = new double[nmesh[0]*nmesh[1]];

	for(int p = 0; p < nmesh[0]; p++){
		for(int nx = 0; nx < nmesh[0]; nx++){
			for(int ny = 0; ny < nmesh[1]; ny++){
				datar[nx*nmesh[1]+ny] = (*Ea)[p][nx][ny].real();
				datai[nx*nmesh[1]+ny] = (*Ea)[p][nx][ny].imag();
			}
		}
		fwrite(datar, sizeof(double), nmesh[0]*nmesh[1], fp);
		fwrite(datai, sizeof(double), nmesh[0]*nmesh[1], fp);
	}
	fclose(fp);

	delete[] datar;
	delete[] datai;
}

void HGModalDecomp2D::f_ComputeWholeWigner(double fnorm, vector<double> &data, int rank, int mpiprocesses)
{
	MPI_Status mpistatus;
	int nxy[2], nq[2], indices[NumberWignerUVPrm], npoints;
	vector<int> steps, inistep, finstep;
	mpi_steps(m_anmesh[0], m_anmesh[1], mpiprocesses, &steps, &inistep, &finstep);
	npoints = m_nmesh[0]*m_nmesh[1];

	m_calcstatus->SetSubstepNumber(1, steps[0]);

	for(nq[1] = 0; nq[1] < m_anmesh[1]; nq[1]++){
		indices[WignerUVPrmv] = nq[1];
		for(nq[0] = 0; nq[0] < m_anmesh[0]; nq[0]++){
			indices[WignerUVPrmu] = nq[0];
			int nm = m_anmesh[0]*nq[1]+nq[0];
			if(nm < inistep[rank] || nm > finstep[rank]){
				continue;
			}
			for(nxy[1] = 0; nxy[1] < m_nmesh[1]; nxy[1]++){
				indices[WignerUVPrmV] = nxy[1];
				for(nxy[0] = 0; nxy[0] < m_nmesh[0]; nxy[0]++){
					indices[WignerUVPrmU] = nxy[0];
					int iindex = m_wig4d->GetTotalIndex(indices);
					data[iindex] = fnorm*GetWignerAt(nxy, nq, m_nmesh, m_anmesh);
				}
			}
			m_calcstatus->AdvanceStep(1);
		}
	}

	if(mpiprocesses > 1){
		double *wsmpi = new double[data.size()];
		for(int n = 0; n < (int)data.size(); n++){
			wsmpi[n] = data[n];
		}
		for(int k = 1; k < mpiprocesses; k++){
			if(rank == 0){
				MPI_Recv(wsmpi+inistep[k]*npoints, steps[k]*npoints, MPI_DOUBLE, k, 0, MPI_COMM_WORLD, &mpistatus);
			}
			else if(rank == k){
				MPI_Send(wsmpi+inistep[k]*npoints, steps[k]*npoints, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
			}
			MPI_Barrier(MPI_COMM_WORLD);
		}
		MPI_Bcast(wsmpi, m_anmesh[0]*m_anmesh[1]*npoints, MPI_DOUBLE, 0, MPI_COMM_WORLD);
		for(int n = 0; n < (int)data.size(); n++){
			data[n] = wsmpi[n];
		}
		delete[] wsmpi;
	}
}
